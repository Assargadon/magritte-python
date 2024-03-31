from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.ext.hybrid import hybrid_property

from MagritteSQLAlchemy.experiments.fieldsmapper import FieldsMapper
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription


def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:

    if not registry:
        registry = sa_registry()
    fields_mapper = FieldsMapper()

    for descriptor in descriptors:
        print(f' ================= > Registering {descriptor.name} ...')

        table = Table(
            descriptor.sa_tableName,
            registry.metadata,
            )

        table.append_column(Column("id", Integer, primary_key=True))

        fields_mapper.map(descriptor, table)

        print(table.c)

        print(" ============================================================= ")

        properties_to_map = {}
        for desc in filter(lambda x: x.sa_storable, descriptor.children):
            print(f'desc = {desc}, desc.name = {desc.name}, is reference = {isinstance(desc, MAReferenceDescription)}')
            if not isinstance(desc, MAReferenceDescription):
                print(f' ... sa_attrName = {desc.sa_attrName}')
                properties_to_map[desc.sa_attrName] = table.c[desc.name]
                
        registry.map_imperatively(
            descriptor.kind,
            table,
            properties=properties_to_map,
            )

    return registry
