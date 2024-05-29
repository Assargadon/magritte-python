import logging
from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry

from MagritteSQLAlchemy.imperative.fieldsmapper import FieldsMapper
from MagritteSQLAlchemy.imperative.propmapper import PropMapper

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
        logger.debug(f' ================= > Creating table for {descriptor.name} ...')
        # table stub
        table = Table(
            descriptor.sa_tableName,
            registry.metadata,
            )

        # map scalar fields
        fields_mapper.map(descriptor, table)

        # add missing primary keys
        table = add_missing_primary_keys(table)

        logger.debug(f'Table columns for {descriptor.name}: {table.c}')
        logger.debug(f' ================= > Created table for {descriptor.name} ...')

    prop_mapper = PropMapper()
    for descriptor in descriptors:
        logger.debug(f' ================= > Mapping tables with properties for {descriptor.name} ...')

        logger.debug(f' ----------------- > Constructing properties and foreign keys...')
        properties_to_map = prop_mapper.map(descriptor, registry.metadata.tables)
        logger.debug(f' Properties to map: {properties_to_map}')

        logger.debug(f' ----------------- > Invoke imperative mapping...')
        registry.map_imperatively(
            descriptor.kind,
            registry.metadata.tables[descriptor.sa_tableName],
            properties=properties_to_map,
            )

        logger.debug(f' ================= > Mapped tables with properties for {descriptor.name} ...')

    return registry
