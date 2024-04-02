from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.orm import relationship

from MagritteSQLAlchemy.experiments.fieldsmapper import FieldsMapper
from MagritteSQLAlchemy.experiments.fkeysmapper import FKeysMapper

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription


def add_missing_primary_keys(table: Table) -> Table:
    if not any([col.primary_key for col in table.c]):
        table.append_column(Column("id", Integer, primary_key=True))
    return table

def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:

    if not registry:
        registry = sa_registry()

    registered_tables = {}
    fields_mapper = FieldsMapper()
    for descriptor in descriptors:

        # table stub
        table = Table(
            descriptor.sa_tableName,
            registry.metadata,
            )

        # map scalar fields
        fields_mapper.map(descriptor, table)

        # add missing primary keys
        table = add_missing_primary_keys(table)

        registered_tables[descriptor.sa_tableName] = table
        print(table.c)

    fkeys_mapper = FKeysMapper()
    for descriptor in descriptors:
        # add foreign keys
        fkeys_mapper.map(descriptor, registered_tables) 

    for descriptor in descriptors:
        print(f' ================= > Registering {descriptor.name} ...')

        properties_to_map = {}
        table = registered_tables[descriptor.sa_tableName]
        for desc in filter(lambda x: x.sa_storable, descriptor.children):
            if not isinstance(desc, MAReferenceDescription) or (isinstance(desc, MASingleOptionDescription) and not isinstance(desc.reference, MAContainer)):
                print(f' Mapping scalar attribute = {desc.sa_attrName}')
                properties_to_map[desc.sa_attrName] = table.c[desc.sa_fieldName]
            if isinstance(desc, MAToOneRelationDescription) and isinstance(desc.reference, MAContainer):
                print(f' Mapping REFERENCE attribute = {desc.sa_attrName}')
                table = registered_tables[descriptor.sa_tableName]
                properties_to_map[desc.sa_attrName] = relationship(desc.reference.kind)
                
        registry.map_imperatively(
            descriptor.kind,
            table,
            properties=properties_to_map,
            )

    return registry
