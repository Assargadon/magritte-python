from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry

def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:
    if not registry:
        registry = sa_registry()
    for descriptor in descriptors:
        print(descriptor.name)

        table = Table(
            descriptor.name,
            registry.metadata,
            Column("id", Integer, primary_key=True),
            )

        print(table.c)

        '''
        registry.map_imperatively(descriptor.cls, descriptor.table)
        for rel in descriptor.relations:
            registry.map_imperatively(rel.cls, rel.table, properties=rel.properties)
        '''

    return registry
