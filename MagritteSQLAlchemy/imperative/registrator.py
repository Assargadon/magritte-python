import logging
from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.orm import relationship

from MagritteSQLAlchemy.imperative.fieldsmapper import FieldsMapper
from MagritteSQLAlchemy.imperative.fkeysmapper import FKeysMapper

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
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
        
    prop_mapper = PropMapper()
    for descriptor in descriptors:
        prop_mapper.map(descriptor, registry)

    return registry
