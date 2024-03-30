from sqlalchemy import Table, Column, Integer, String

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
        self.visitAll(description.children)

    def visitIntDescription(self, description):
        print(f'visitIntDescription {description.name}')
        self.table.append_column(Column(description.name, Integer))

    def visitStringDescription(self, description):
        print(f'visitStringDescription {description.name}')
        self.table.append_column(Column(description.name, String(250)))