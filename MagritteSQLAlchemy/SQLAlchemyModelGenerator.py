from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column
from sqlalchemy import Boolean, Date, DateTime, Integer, Interval, Float, String, Text, Time, ForeignKeyConstraint

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.visitors.MAVisitor_class import MAVisitor


class SqlAlchemyFieldExtractorFromMAElementVisitor(MAVisitor):
    def visitBooleanDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Boolean, element_description=element_description)

    def visitDateDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Date, element_description=element_description)

    def visitDateAndTimeDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=DateTime, element_description=element_description)

    def visitDurationDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Interval, element_description=element_description)

    def visitIntDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Integer, element_description=element_description)

    def visitFloatDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Float, element_description=element_description)

    def visitMemoDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Text, element_description=element_description)

    def visitStringDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=String, element_description=element_description)

    def visitTimeDescription(self, element_description: MAElementDescription):
        return self.make_result(sql_type=Time, element_description=element_description)

    def visitElementDescription(self, element_description: MAElementDescription):
        raise f"Cannot map type: '{element_description.kind}' to the Sql Alchemy: a certain type mapper is unimplemented"

    def make_result(self, sql_type, element_description: MAElementDescription):
        return dict(
            type=sql_type
            , name=element_description.fieldName
            , primary_key=element_description.isPrimaryKey
            , nullable=element_description.required)


class SqlAlchemyForeignVisitor(SqlAlchemyFieldExtractorFromMAElementVisitor):
    def visitToOneRelationDescription(self, element_description: MARelationDescription):
        parent_visitor = SqlAlchemyFieldExtractorFromMAElementVisitor()
        reference = element_description.reference

        for relation_field in reference.children:
            if relation_field.isPrimaryKey:
                field_info = parent_visitor.visit(relation_field)
                field_name = reference.tableName + '_' + field_info["name"]
                return dict(type=field_info["type"], name=field_name)


class DefaultBase(DeclarativeBase):
    pass


class SQLAlchemyModelGenerator(MAVisitor):
    _base_class = None
    _field_extractor = None
    _model_desc = None
    _table_args = []

    def __init__(self, base_class=DefaultBase, field_extractor=SqlAlchemyFieldExtractorFromMAElementVisitor()):
        self._field_extractor = field_extractor
        self._base_class = base_class

    @property
    def base_class(self):
        return self._base_class

    def visitContainer(self, container: MAContainer):
        self._table_args = []
        self._model_desc = {'__tablename__': container.tableName}
        self.visitAll(container.children)
        if len(self._table_args) > 0:
            self._model_desc['__table_args__'] = tuple(self._table_args)
        return type(container.name, (self._base_class,), self._model_desc)

    def generate_model(self, container: MAContainer):
        self.visitContainer(container)

    def visitElementDescription(self, element_description: MAElementDescription):
        self.make_column_from_element(self._field_extractor.visit(element_description))

    def visitToManyRelationDescription(self, element_description: MARelationDescription):
        self._model_desc[element_description.fieldName] = relationship(
            element_description.reference.tableName
            , back_populates=element_description.reference.name)

    def visitToOneRelationDescription(self, element_description: MARelationDescription):
        foreign_visitor = SqlAlchemyForeignVisitor()
        reference = element_description.reference
        self._model_desc[element_description.fieldName] = relationship(reference.tableName,
                                                                       back_populates=reference.name)

        foreign_keys = []
        foreign_fields_name = []
        for relation_field in reference.children:
            if relation_field.isPrimaryKey:
                field_info = foreign_visitor.visit(relation_field)
                foreign_field_name = reference.tableName + '_' + field_info["name"]
                foreign_key = reference.tableName + '.' + field_info["name"]
                is_primary_key = relation_field.isPrimaryKey
                self.make_column(field_name=foreign_field_name, sqlType=field_info["type"],
                                 primary_key=is_primary_key)
                foreign_keys.append(foreign_key)
                foreign_fields_name.append(foreign_field_name)
        self._table_args.append(ForeignKeyConstraint(foreign_fields_name, foreign_keys))

    def make_column(self, field_name: str, sqlType, nullable=False, primary_key=False):
        self._model_desc[field_name] = mapped_column(sqlType, nullable=nullable, primary_key=primary_key)

    def make_column_from_element(self, field_info):
        self.make_column(field_name=field_info['name'], sqlType=field_info['type']
                         , nullable=field_info['nullable'], primary_key=field_info['primary_key'])
