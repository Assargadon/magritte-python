import logging

from sqlalchemy import Table
from sqlalchemy.orm import relationship, registry as sa_registry

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor

logger = logging.getLogger(__name__)


class PropMapper(MAVisitor):
    def __init__(self):
        self._root_desc = None
        self._table = None
        self._properties_to_map = None

    @staticmethod
    def _find_attribute_for_back_populates(myKind, ref_desc: MAContainer):
        for desc in ref_desc.children:
            if isinstance(desc, MAReferenceDescription) and desc.reference.kind == myKind:
                return desc.sa_attrName
        return None

    def get_fkey_for_property(self, source_table: Table, property_name: str):
        logger.debug(f'Getting foreign key from {source_table.name} for property name {property_name}.')
        fkeys = []
        for fkey in source_table.foreign_keys:
            logger.debug(f"Testing foreign key from {source_table.name} - {fkey.parent}:")
            logger.debug(f"{fkey.__dict__}")
            if fkey.parent is not None:
                logger.debug(f"fkey.parent = {fkey.parent}")
                logger.debug(f"fkey.parent.name = {fkey.parent.name}")
                if fkey.parent.name and fkey.parent.name.startswith(property_name):
                    logger.debug(
                        f"Foreign key from {source_table.name} for property name {property_name} found."
                        f" Column: {(id(fkey.parent), fkey.parent)}"
                        )
                    fkeys.append(fkey.parent)
                else:
                    logger.debug(f"Foreign key from {source_table.name} for property name {property_name} does not match.")
        if not fkeys:
            logger.debug(f'Foreign key from {source_table.name} for property name {property_name} does not exist.')
        else:
            return fkeys

    def map(self, description: MAContainer, table: Table) -> dict:
        if not isinstance(description, MAContainer):
            raise ValueError(f'{description} is not a container')
        if table is None:
            raise ValueError('Table is not provided')

        self._root_desc = description
        self._table = table
        self._properties_to_map = {}

        self.visit(description)

        return self._properties_to_map

    def visitDescription(self, description):
        logger.warning(f'Description {description} not supported')

    def visitContainer(self, description):
        # logger.debug(f'visitContainer {description.name}')
        self.visitAll(filter(lambda x: x.sa_storable, description.children))

    def visitElementDescription(self, description):
        # logger.debug(f'visitElementDescription {description.name}')
        logger.debug(
            f"Mapping scalar attribute '{description.sa_attrName}' "
            f"to table column '{self._table.c[description.sa_fieldName]}'"
            )
        self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]

    def visitSingleOptionDescription(self, description):
        # logger.debug(f'visitSingleOptionDescription {description.name}')
        reference = description.reference
        # if reference is scalar type, i.e. not subclass of MAContainer, then it's just a scalar field
        if not isinstance(reference, MAContainer):
            logger.debug(
                f"Mapping scalar attribute '{description.sa_attrName}' "
                f"to table column '{self._table.c[description.sa_fieldName]}'"
                )
            self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]
        else:
            back_populates = self._find_attribute_for_back_populates(self._root_desc.kind, reference)
            foreign_keys = self.get_fkey_for_property(self._table, description.name)
            logger.debug(
                f"Mapping SINGLE OPTION to-object attribute '{description.sa_attrName}' "
                f"as relationship to '{reference.kind}' "
                f"with back_populates = '{back_populates}'"
                f"and foreign_keys = '{foreign_keys}'"
                )
            self._properties_to_map[description.sa_attrName] = relationship(
                reference.kind, back_populates=back_populates, # foreign_keys=foreign_keys
                )

    def visitToOneRelationDescription(self, description):
        # logger.debug(f'visitToOneRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        back_populates = self._find_attribute_for_back_populates(self._root_desc.kind, description.reference)
        foreign_keys = self.get_fkey_for_property(self._table, description.name)
        logger.debug(
            f"Mapping TO ONE attribute '{description.sa_attrName}' "
            f"as relationship to '{description.reference.kind}' "
            f"with back_populates = '{back_populates}'"
            f"and foreign_keys = '{foreign_keys}'"
            )
        self._properties_to_map[description.sa_attrName] = relationship(
            description.reference.kind, back_populates=back_populates, foreign_keys=foreign_keys
            )

    def visitToManyRelationDescription(self, description):
        # logger.debug(f'visitToManyRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        back_populates = self._find_attribute_for_back_populates(self._root_desc.kind, description.reference)
        logger.debug(
            f"Mapping TO MANY attribute '{description.sa_attrName}' "
            f"as relationship to '{description.reference.kind}' "
            f"with back_populates = '{back_populates}'"
            )
        self._properties_to_map[description.sa_attrName] = relationship(description.reference.kind, back_populates=back_populates)
