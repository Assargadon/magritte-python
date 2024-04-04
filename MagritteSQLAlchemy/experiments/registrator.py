import logging
from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.orm import relationship

from MagritteSQLAlchemy.experiments.fieldsmapper import FieldsMapper
from MagritteSQLAlchemy.experiments.fkeysmapper import FKeysMapper

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription

logger = logging.getLogger(__name__)


def add_missing_primary_keys(table: Table) -> Table:
    if(len(table.primary_key) == 0):
        logger.debug(f'Adding ID as default primary key to table {table.name} ({table.primary_key})')
        table.append_column(Column("id", Integer, primary_key=True))
    return table

def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:

    if not registry:
        registry = sa_registry()

    fields_mapper = FieldsMapper()
    for descriptor in descriptors:

        # table stub
        table = Table(
            descriptor.sa_tableName,
            registry.metadata,
            )

        logger.debug(f' ==== registry.metadata.tables ===')
        logger.debug(f'{registry.metadata.tables}')
        logger.debug(f' =================================')

        # map scalar fields
        fields_mapper.map(descriptor, table)

        # add missing primary keys
        table = add_missing_primary_keys(table)

        logger.debug(table.c)

    fkeys_mapper = FKeysMapper()
    for descriptor in descriptors:
        # add foreign keys
        fkeys_mapper.map(descriptor, registry.metadata.tables)


    def find_attribute_for_back_populates(myKind, reference_descriptor_container):
        for desc in reference_descriptor_container.children:
            if isinstance(desc, MAReferenceDescription) and desc.reference.kind == myKind:
                return desc.sa_attrName
        return None

    for descriptor in descriptors:
        logger.debug(f' ================= > Registering {descriptor.name} ...')

        properties_to_map = {}
        table = registry.metadata.tables[descriptor.sa_tableName]
        for desc in filter(lambda x: x.sa_storable, descriptor.children):
            if not isinstance(desc, MAReferenceDescription) or (isinstance(desc, MASingleOptionDescription) and not isinstance(desc.reference, MAContainer)):
                logger.debug(f' Mapping scalar attribute = {desc.sa_attrName}')
                properties_to_map[desc.sa_attrName] = table.c[desc.sa_fieldName]
            if isinstance(desc, MAToOneRelationDescription) and isinstance(desc.reference, MAContainer):
                logger.debug(f' Mapping TO ONE attribute = {desc.sa_attrName}')
                back_populates_attr = find_attribute_for_back_populates(descriptor.kind, desc.reference)
                properties_to_map[desc.sa_attrName] = relationship(desc.reference.kind, back_populates=back_populates_attr)
            if isinstance(desc, MASingleOptionDescription) and isinstance(desc.reference, MAContainer):
                back_populates_attr = find_attribute_for_back_populates(descriptor.kind, desc.reference)
                logger.debug(f' Mapping SINGLE OPTION to-object attribute = {desc.sa_attrName} back_populates_attr = {back_populates_attr}')
                properties_to_map[desc.sa_attrName] = relationship(desc.reference.kind, back_populates=back_populates_attr)
            if isinstance(desc, MAToManyRelationDescription) and isinstance(desc.reference, MAContainer):
                logger.debug(f' Mapping TO MANY attribute = {desc.sa_attrName}')
                back_populates_attr = find_attribute_for_back_populates(descriptor.kind, desc.reference)
                properties_to_map[desc.sa_attrName] = relationship(desc.reference.kind, back_populates=back_populates_attr)
                
        registry.map_imperatively(
            descriptor.kind,
            table,
            properties=properties_to_map,
            )

    return registry
