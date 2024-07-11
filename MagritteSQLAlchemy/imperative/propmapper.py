import logging
from typing import List

from sqlalchemy import Table, ForeignKeyConstraint, Column
from sqlalchemy.orm import relationship

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor

logger = logging.getLogger(__name__)


class PropMapper(MAVisitor):
    """Properties Mapper.
    Maps properties of a model descriptor to SQLAlchemy table columns and relationships.
    For reference fields, it creates foreign keys and relationships.
    ForeignKey naming convention:
    - for to-one relations: <description.name>_<target_table_PK_name>
    - for to-many relations: look for back reference
        - if found, use <backref's description.name>_<target_table_PK_name>
        - if not found, use <description.name>_<root_description.name>_<target_table_PK_name>
    """
    def __init__(self):
        self._root_desc = None
        self._table = None
        self._registered_tables = None
        self._properties_to_map = None

    @staticmethod
    def _find_backref_desc(myKind, ref_desc: MAContainer):
        for desc in ref_desc.children:
            if isinstance(desc, MAReferenceDescription) and desc.reference.kind == myKind:
                return desc
        return None

    def _fkey_already_exists(self, source_table: Table, property_name: str, target_table: Table):
        logger.debug(
            f'Checking if foreign key from {source_table.name} for property name {property_name}'
            f' to {target_table.name} already exists.'
            )
        for fkey in source_table.foreign_keys:
            if fkey.references(target_table):
                if fkey.parent is not None:
                    if fkey.parent.name and fkey.parent.name.startswith(property_name):
                        logger.debug(
                            f'Foreign key from {source_table.name} for property name {property_name}'
                            f' to {target_table.name} found: {fkey}'
                            )
                        return True
        logger.debug(
            f'Foreign key from {source_table.name} for property name {property_name}'
            f' to {target_table.name} does not exist.'
            )
        return False

    def _append_fkey(self, property_name: str, source_table: Table, target_table: Table) -> List[Column] | None:
        logger.debug(
            f'Adding foreign key from {source_table.name} for property name {property_name} to {target_table.name}'
            )
        # if self.is_fkey_already_exists(source_table, property_name, target_table):
        if self._fkey_already_exists(source_table, property_name, target_table):
            logger.debug(f'Foreign key from {source_table.name} to {target_table.name} already exists')
            return

        # first, let's add all the columns to the source_table that are part of the foreign key
        primary_keys_of_target = target_table.primary_key
        if (primary_keys_of_target is None or len(primary_keys_of_target) == 0):
            raise ValueError(f'Target table {target_table.name} does not have primary keys')

        fkey_columns = []
        for column in primary_keys_of_target:
            fkey_column_name = f'{property_name}_{column.name}'
            if fkey_column_name in source_table.columns:
                fkey_column = source_table.columns[fkey_column_name]
            else:
                fkey_column = Column(fkey_column_name, column.type)
                source_table.append_column(fkey_column)
            fkey_columns.append(fkey_column)

        logger.debug(
            f'Added foreign key columns to {source_table.name}: '
            f'{[(id(column), column) for column in fkey_columns]}'
            )

        # now, let's add the foreign key constraint to the source_table)
        source_table.append_constraint(
            ForeignKeyConstraint(
                columns=fkey_columns,
                refcolumns=primary_keys_of_target
                )
            )

        return fkey_columns

    def map(self, description: MAContainer, registered_tables: dict) -> dict:
        if not isinstance(description, MAContainer):
            raise ValueError(f'{description} is not a container')
        if registered_tables is None:
            raise ValueError('registered_tables not provided')

        self._root_desc = description
        self._registered_tables = registered_tables
        self._table = registered_tables[description.sa_tableName]
        self._properties_to_map = {}

        self.visit(description)

        return self._properties_to_map

    def visitDescription(self, description):
        logger.warning(f'Description {description} is not supported in PropMapper')

    def visitContainer(self, description):
        # logger.debug(f'visitContainer {description.name}')
        self.visitAll(filter(lambda x: x.sa_storable, description.children))

    def visitElementDescription(self, description):
        # logger.debug(f'visitElementDescription {description.name}')
        logger.debug(
            f"Mapping scalar attribute '{description.sa_attrName}' "
            f"to table column '{self._table.c[description.sa_fieldName]}'"
            )
        self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]

    def visitSingleOptionDescription(self, description):
        # logger.debug(f'visitSingleOptionDescription {description.name}')
        reference = description.reference
        # if reference is scalar type, i.e. not subclass of MAContainer, then it's just a scalar field
        if not isinstance(reference, MAContainer):
            logger.debug(
                f"Mapping scalar attribute '{description.sa_attrName}' "
                f"to table column '{self._table.c[description.sa_fieldName]}'"
                )
            self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]
        else:
            target_table = self._registered_tables[description.reference.sa_tableName]
            foreign_keys = self._append_fkey(description.name, self._table, target_table)
            backref = self._find_backref_desc(self._root_desc.kind, reference)
            back_populates = backref.sa_attrName if backref else None
            logger.debug(
                f"Mapping SINGLE OPTION to-object attribute '{description.sa_attrName}' "
                f"as relationship to '{reference.kind}' "
                f"with back_populates = '{back_populates}'"
                f"and foreign_keys = '{foreign_keys}'"
                )
            self._properties_to_map[description.sa_attrName] = relationship(
                reference.kind, back_populates=back_populates, foreign_keys=foreign_keys
                )

    def visitToOneRelationDescription(self, description):
        # logger.debug(f'visitToOneRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        target_table = self._registered_tables[description.reference.sa_tableName]
        foreign_keys = self._append_fkey(description.name, self._table, target_table)
        backref = self._find_backref_desc(self._root_desc.kind, description.reference)
        back_populates = backref.sa_attrName if backref else None
        logger.debug(
            f"Mapping TO ONE attribute '{description.sa_attrName}' "
            f"as relationship to '{description.reference.kind}' "
            f"with back_populates = '{back_populates}'"
            f"and foreign_keys = '{foreign_keys}'"
            )
        self._properties_to_map[description.sa_attrName] = relationship(
            description.reference.kind, back_populates=back_populates, foreign_keys=foreign_keys
            )

    def visitToManyRelationDescription(self, description):
        # logger.debug(f'visitToManyRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        source_table = self._registered_tables[description.reference.sa_tableName]
        backref = self._find_backref_desc(self._root_desc.kind, description.reference)
        back_populates = backref.sa_attrName if backref else None
        fkey_name = backref.name if backref else f"{description.name}_" + self._root_desc.name.lower()
        foreign_keys = self._append_fkey(fkey_name, source_table, self._table)
        logger.debug(
            f"Mapping TO MANY attribute '{description.sa_attrName}' "
            f"as relationship to '{description.reference.kind}' "
            f"with back_populates = '{back_populates}'"
            f"and foreign_keys = '{foreign_keys}'"
            )
        self._properties_to_map[description.sa_attrName] = relationship(
            description.reference.kind, back_populates=back_populates, foreign_keys=foreign_keys
            )
