import logging
from sqlalchemy import Table, Column, Integer, String, Date, Boolean, DateTime, Text

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.visitors.MAVisitor_class import MAVisitor
from sqlalchemy.orm import registry as sa_registry

logger = logging.getLogger(__name__)


class FieldsMapper(MAVisitor):
    def __init__(self):
        self.table = None

    def map(self, description: MAContainer, table: Table) -> Table:
        self.table = table
        self.visit(description)
        return self.table

    def visitDescription(self, description):
        logger.warning(f'Description {description} not supported')

    def visitContainer(self, description):
        logger.debug(f'visitContainer {description.name}')
        self.visitAll(filter(lambda x: x.sa_storable, description.children))

    def visitIntDescription(self, description):
        logger.debug(f'visitIntDescription {description.name}')
        self.table.append_column(Column(
            description.sa_fieldName, Integer,
            primary_key=description.sa_isPrimaryKey, nullable=(not description.required)
            ))

    def visitStringDescription(self, description):
        logger.debug(f'visitStringDescription {description.name}')
        self.table.append_column(Column(
            description.sa_fieldName, Text,
            primary_key=description.sa_isPrimaryKey, nullable=(not description.required)
            ))

    def visitDateDescription(self, description):
        logger.debug(f'visitDateDescription {description.name}')
        self.table.append_column(Column(
            description.sa_fieldName, Date,
            primary_key=description.sa_isPrimaryKey, nullable=(not description.required)
            ))

    def visitDateAndTimeDescription(self, description):
        logger.debug(f'visitDateAndTimeDescription {description.name}')
        self.table.append_column(Column(
            description.sa_fieldName, DateTime,
            primary_key=description.sa_isPrimaryKey, nullable=(not description.required)
            ))

    def visitBooleanDescription(self, description):
        logger.debug(f'visitBooleanDescription {description.name}')
        self.table.append_column(Column(
            description.sa_fieldName, Boolean,
            primary_key=description.sa_isPrimaryKey, nullable=(not description.required)
            ))
        
    def visitSingleOptionDescription(self, description):
        logger.debug(f'visitSingleOptionDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            logger.debug('!!!! reference is scalar !!!')
            reference = description.reference.__copy__()
            reference.name = description.name
            reference.sa_fieldName = description.sa_fieldName
            reference.sa_attrName = description.sa_attrName
            reference.sa_storable = description.sa_storable
            reference.sa_isPrimaryKey = description.sa_isPrimaryKey
            reference.required = description.required
            self.visit(reference)
        else:
            logger.debug('!!!! reference is object !!!')
            for child_desc in description.reference.children:
                if child_desc.sa_isPrimaryKey:
                    child_copy = child_desc.__copy__()
                    child_copy.sa_fieldName = f'{description.sa_fieldName}_{child_desc.sa_fieldName}'
                    child_copy.sa_isPrimaryKey = description.sa_isPrimaryKey
                    child_copy.required = description.required
                    self.visit(child_copy)

    def visitToOneRelationDescription(self, description):
        logger.debug(f'visitToOneRelationDescription {description.name}')
        for child_desc in description.reference.children:
            if child_desc.sa_isPrimaryKey:
                child_copy = child_desc.__copy__()
                child_copy.sa_fieldName = f'{description.sa_fieldName}_{child_desc.sa_fieldName}'
                child_copy.sa_isPrimaryKey = description.sa_isPrimaryKey
                child_copy.required = description.required
                self.visit(child_copy)
