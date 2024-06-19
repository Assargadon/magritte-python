import logging

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.visitors.MAReferencedDataWriterReader_visitors import (
    MAReferencedDataHumanReadableSerializer,
    MAReferencedDataHumanReadableDeserializer,
    )
from MagritteSQLAlchemy.imperative import registrator

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


class Port:
    def __init__(self):
        self.numofport = None
        self.features = []


class Feature:
    def __init__(self):
        self.name = None
        self.value = None


port_desc = MAContainer(kind=Port, name="Port")
feature_desc = MAContainer(kind=Feature, name="Feature")

port_desc.setChildren([
    MAIntDescription(name="numofport", accessor=MAAttrAccessor("numofport"), required=True),
    MAToManyRelationDescription(
        name="features",
        accessor=MAAttrAccessor("features"),
        classes=[Feature],
        reference=feature_desc
    )
])

feature_desc.setChildren([
    MAStringDescription(name="name", accessor=MAAttrAccessor("name"), required=True),
    MAStringDescription(name="value", accessor=MAAttrAccessor("value"), required=True)
])

descriptions = [port_desc, feature_desc]

if __name__ == '__main__':

    port = Port()
    feature = Feature()

    port.numofport = 81

    feature.name = "feature_0"
    feature.value = "value_0"

    features = []
    logger.error(f"id(features): {hex(id(features))}, features = {features}")
    port.features = features
    logger.error(f"id(port.features): {hex(id(port.features))}, port.features = {port.features}")
    features.append(feature)
    logger.error(f"port.features[0].name: {port.features[0].name}")

    # ============================================================================================
    logger.error(f" Enabling ORM mapping ")
    registry = registrator.register(*descriptions)

    port = Port()
    feature = Feature()

    port.numofport = 81

    feature.name = "feature_0"
    feature.value = "value_0"

    features = []
    logger.error(f"id(features): {hex(id(features))}, features = {features}")
    port.features = features
    logger.error(f"id(port.features): {hex(id(port.features))}, port.features = {port.features}")
    features.append(feature)
    logger.error(f"port.features[0].name: {port.features[0].name}")
