import logging
from sqlalchemy import Table, Column, Integer, String, Date, Boolean, DateTime

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.visitors.MAVisitor_class import MAVisitor
from sqlalchemy.orm import registry as sa_registry
from sqlalchemy.schema import ForeignKeyConstraint

logger = logging.getLogger(__name__)


class FKeysMapper(MAVisitor):
    def __init__(self):
        self.table = None

    def map(self, description: MAContainer, registered_tables: dict):
        self.root_desc = description
        self.registered_tables = registered_tables
        self.my_table = self.registered_tables[description.sa_tableName]
        self.visit(description)

    # adds a foreign key to the source_table which points to the target_table with the property_name as part of the fields for the foreign key columns
    def append_fkey(self, property_name: String, source_table: Table, target_table: Table):
        property_name = property_name.lower()
        logger.debug(f'Adding foreign key from {source_table.name} for property name {property_name} to {target_table.name}')
        # if self.is_fkey_already_exists(source_table, property_name, target_table):
        if self.is_fkey_already_exists(source_table, property_name, target_table):
            logger.debug(f'Foreign key from {source_table.name} to {target_table.name} already exists')
            return

        # first, let's add all the columns to the source_table that are part of the foreign key
        primary_keys_of_target = target_table.primary_key
        if(primary_keys_of_target is None or len(primary_keys_of_target) == 0):
            raise ValueError(f'Target table {target_table.name} does not have primary keys')

        fkey_columns = []
        for column in primary_keys_of_target:
            fkey_column_name = f'{property_name}_{column.name}'
            fkey_column = Column(fkey_column_name, column.type)

            source_table.append_column(fkey_column)
            fkey_columns.append(fkey_column)

        logger.debug(
            f'Added foreign key columns to {source_table.name}: '
            f'{[(id(column), column) for column in fkey_columns]}'
            )
         
        # now, let's add the foreign key constraint to the source_table)
        source_table.append_constraint(
            ForeignKeyConstraint(
                columns = fkey_columns,
                refcolumns = primary_keys_of_target
            )
        )

    def is_fkey_already_exists(self, source_table: Table, property_name: String, target_table: Table):
        logger.debug(f'Checking if foreign key from {source_table.name} for property name {property_name} to {target_table.name} already exists.')
        for fkey in source_table.foreign_keys:
            logger.debug(f"fkey.references({target_table}) = {fkey.references(target_table)}")
            if fkey.references(target_table):
                logger.debug(f"Foreign key from {source_table.name} to {target_table.name} is {fkey}:")
                logger.debug(f"{fkey.__dict__}")
                if fkey.parent is not None:
                    logger.debug(f"fkey.parent = {fkey.parent}")
                    logger.debug(f"fkey.parent.name = {fkey.parent.name}")
                    if fkey.parent.name and fkey.parent.name.startswith(property_name):
                        return True
        logger.debug(f'Foreign key from {source_table.name} for property name {property_name} to {target_table.name} does not exist.')
        return False


    def visitDescription(self, description):
        logger.warning(f'Description {description} not supported in FKeysMapper')

    def visitContainer(self, description):
        logger.debug(f'visitContainer {description.name}')
        self.visitAll(description.children)  # no filtering?


    def visitToOneRelationDescription(self, description):
        logger.debug(f'visitToOneRelationDescription {description.name}')
        target_table = self.registered_tables[description.reference.sa_tableName]
        self.append_fkey(description.name, self.my_table, target_table)

    def visitSingleOptionDescription(self, description):
        logger.debug(f'visitSingleOptionDescription {description.name}')
        if isinstance(description.reference, MAContainer):
            logger.debug('!!!! reference is container !!!')
            self.visitToOneRelationDescription(description)

    def visitToManyRelationDescription(self, description):
        logger.debug(f'visitToManyRelationDescription {description.name}')
        target_table = self.registered_tables[description.reference.sa_tableName]
        self.append_fkey(self.root_desc.name, target_table, self.my_table)
