from sqlalchemy import Table, Column, Integer, String, Date, Boolean, DateTime

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.visitors.MAVisitor_class import MAVisitor
from sqlalchemy.orm import registry as sa_registry


class FieldsMapper(MAVisitor):
    def __init__(self):
        self.table = None

    def map(self, description: MAContainer, table: Table) -> Table:
        self.table = table
        self.visit(description)
        return self.table

    def visitDescription(self, description):
        print(f'Description {description} not supported')

    def visitContainer(self, description):
        print(f'visitContainer {description.name}')
        self.visitAll(filter(lambda x: x.sa_storable, description.children))

    def visitIntDescription(self, description):
        print(f'visitIntDescription {description.name}')
        self.table.append_column(Column(description.sa_fieldName, Integer))

    def visitStringDescription(self, description):
        print(f'visitStringDescription {description.name}')
        self.table.append_column(Column(description.sa_fieldName, String(250)))

    def visitDateDescription(self, description):
        print(f'visitDateDescription {description.name}')
        self.table.append_column(Column(description.sa_fieldName, Date))

    def visitDateAndTimeDescription(self, description):
        print(f'visitDateAndTimeDescription {description.name}')
        self.table.append_column(Column(description.sa_fieldName, DateTime))

    def visitBooleanDescription(self, description):
        print(f'visitBooleanDescription {description.name}')
        self.table.append_column(Column(description.sa_fieldName, Boolean))
        
    def visitSingleOptionDescription(self, description):
        print(f'visitSingleOptionDescription {description.name}')
        reference = description.reference.__copy__()
        reference.name = description.name
        reference.sa_fieldName = description.sa_fieldName
        reference.sa_attrName = description.sa_attrName
        reference.sa_storable = description.sa_storable
        reference.sa_isPrimaryKey = description.sa_isPrimaryKey
        # if reference is scalar type, i.e. not subclass of MAContainer, then it's just a scalar field
        if not isinstance(reference, MAContainer):
            print('!!!! reference is scalar !!!')
            self.visit(reference)
        else:
            print('!!!! reference is container !!!')
        #else:
            # if reference is a container, then it's a reference field
        #    self.table.append_column(Column(description.name, Integer, ForeignKey(reference.sa_tableName + ".id")))
