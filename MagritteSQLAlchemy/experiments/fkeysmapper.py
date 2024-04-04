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
        self.registered_tables = registered_tables
        self.my_table = self.registered_tables[description.sa_tableName]
        self.visit(description)

    # adds a foreign key to the source_table which points to the target_table with the property_name as part of the fields for the foreign key columns
    def append_fkey(self, property_name: String, source_table: Table, target_table: Table):
        if self.is_fkey_already_exists(source_table, target_table):
            print(f'Foreign key from {source_table.name} to {target_table.name} already exists')
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
         
        # now, let's add the foreign key constraint to the source_table)
        source_table.append_constraint(
            ForeignKeyConstraint(
                columns = fkey_columns,
                refcolumns = primary_keys_of_target
            )
        )

    def is_fkey_already_exists(self, source_table: Table, target_table: Table):
    # TODO: this would not work with SEVERAL relations from one table to another - but it's rare case
    # it would need to identify the mere _relation_ between the tables, not just the presence of SOME foreign key

        for fkey in source_table.foreign_keys:
            if fkey.references(target_table):
                return True
        return False


    def visitDescription(self, description):
        logger.warning(f'Description {description} not supported in FKeysMapper')

    def visitContainer(self, description):
        logger.debug(f'visitContainer {description.name}')
        self.visitAll(description.children)


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
        self.append_fkey(description.name, target_table, self.my_table)
