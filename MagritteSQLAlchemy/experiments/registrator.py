from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry

from MagritteSQLAlchemy.experiments.fieldsmapper import FieldsMapper


def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:

    if not registry:
        registry = sa_registry()
    fields_mapper = FieldsMapper()

    for descriptor in descriptors:
        print(descriptor.name)

        table = Table(
            descriptor.name,
            registry.metadata,
            )

        table.append_column(Column("id", Integer, primary_key=True))

        fields_mapper.map(descriptor, table)

        print(table.c)

        registry.map_imperatively(
            descriptor.kind,
            table,
            )
        '''
        properties={
            "addresses": relationship(
                Address,
                back_populates="user",
                ),
            "nick": user_table.c.nickname,
            },
        '''

        '''
        registry.map_imperatively(descriptor.cls, descriptor.table)
        for rel in descriptor.relations:
            registry.map_imperatively(rel.cls, rel.table, properties=rel.properties)
        '''

    return registry
