from sqlalchemy import Table, Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from descriptions.MAContainer_class import MAContainer
from visitors.MAVisitor_class import MAVisitor
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
        for desc in description.children:
            setattr(description.kind, desc.name + '_', hybrid_property(
                fget=lambda model: desc.accessor.read(model),
                fset=lambda model, value: desc.accessor.write(model, value),
                ))
        self.visitAll(description.children)

    def visitIntDescription(self, description):
        print(f'visitIntDescription {description.name}')
        self.table.append_column(Column(description.name, Integer))

    def visitStringDescription(self, description):
        print(f'visitStringDescription {description.name}')
        self.table.append_column(Column(description.name, String(250)))

    def visitDateDescription(self, description):
        print(f'visitDateDescription {description.name}')
        self.table.append_column(Column(description.name, Date))

    def visitDateAndTimeDescription(self, description):
        print(f'visitDateAndTimeDescription {description.name}')
        self.table.append_column(Column(description.name, DateTime))

    def visitBooleanDescription(self, description):
        print(f'visitBooleanDescription {description.name}')
        self.table.append_column(Column(description.name, Boolean))
