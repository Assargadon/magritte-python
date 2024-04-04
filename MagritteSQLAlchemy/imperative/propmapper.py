import logging

from sqlalchemy.orm import relationship

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor

logger = logging.getLogger(__name__)


class PropMapper(MAVisitor):
    def __init__(self):
        self._table = None
        self._properties_to_map = None

    def _find_attribute_for_back_populates(self, myKind, ref_desc: MAContainer):
        for desc in ref_desc.children:
            if isinstance(desc, MAReferenceDescription) and desc.reference.kind == myKind:
                return desc.sa_attrName
        return None

    def map(self, description: MAContainer, table) -> dict:
        logger.debug(f' ================= > Registering {description.name} ...')
        if not isinstance(description, MAContainer):
            raise ValueError(f'{description} is not a container')
        if table is None:
            raise ValueError('Table is not provided')
        self._table = table
        self._properties_to_map = {}
        self.visit(description)
        logger.debug(f' Properties to map: {self._properties_to_map}')
        logger.debug(f' ================= > Registered {description.name} ...')
        return self._properties_to_map

    def visitDescription(self, description):
        logger.warning(f'Description {description} not supported')

    def visitContainer(self, description):
        logger.debug(f'visitContainer {description.name}')
        self.visitAll(filter(lambda x: x.sa_storable, description.children))

    def visitElementDescription(self, description):
        logger.debug(f'visitElementDescription {description.name}')
        logger.debug(f' Mapping scalar attribute = {description.sa_attrName}')
        self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]

    def visitSingleOptionDescription(self, description):
        logger.debug(f'visitSingleOptionDescription {description.name}')
        reference = description.reference
        # if reference is scalar type, i.e. not subclass of MAContainer, then it's just a scalar field
        if not isinstance(reference, MAContainer):
            logger.debug(f' Mapping scalar attribute = {description.sa_attrName}')
            self._properties_to_map[description.sa_attrName] = self._table.c[description.sa_fieldName]
        else:
            back_populates = self._find_attribute_for_back_populates(description.kind, description.reference)
            logger.debug(
                f' Mapping SINGLE OPTION to-object attribute = '
                f'{description.sa_attrName} back_populates = {back_populates}'
                )
            self._properties_to_map[description.sa_attrName] = relationship(reference.kind, back_populates=back_populates)

    def visitToOneRelationDescription(self, description):
        logger.debug(f'visitToOneRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        back_populates = self._find_attribute_for_back_populates(description.kind, description.reference)
        logger.debug(f' Mapping TO ONE attribute = {description.sa_attrName}')
        self._properties_to_map[description.sa_attrName] = relationship(description.reference.kind, back_populates=back_populates)

    def visitToManyRelationDescription(self, description):
        logger.debug(f'visitToManyRelationDescription {description.name}')
        if not isinstance(description.reference, MAContainer):
            raise ValueError('Reference is not a container')
        back_populates = self._find_attribute_for_back_populates(description.kind, description.reference)
        logger.debug(f' Mapping TO MANY attribute = {description.sa_attrName}')
        self._properties_to_map[description.sa_attrName] = relationship(description.reference.kind, back_populates=back_populates)
