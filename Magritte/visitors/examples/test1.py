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
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class Host:
    def __init__(self):
        self.ip = None
        self.ports = []


class Port:
    def __init__(self):
        self.host = None
        self.numofport = None
        self.features = []


class Feature:
    def __init__(self):
        self.name = None
        self.value = None


host_desc = MAContainer(kind=Host, name="Host")
port_desc = MAContainer(kind=Port, name="Port")
feature_desc = MAContainer(kind=Feature, name="Feature")

host_desc.setChildren([
    MAStringDescription(name="ip", accessor=MAAttrAccessor("ip"), required=True),
    MAToManyRelationDescription(
        name="ports",
        accessor=MAAttrAccessor("ports"),
        classes=[Port],
        reference=port_desc
    )
])

host_ports_desc = host_desc[1]

port_desc.setChildren([
    MAIntDescription(name="numofport", accessor=MAAttrAccessor("numofport"), required=True),
    MAToOneRelationDescription(
        name="host",
        accessor=MAAttrAccessor("host"),
        required=True,
        classes=[Host],
        reference=host_desc
    ),
    MAToManyRelationDescription(
        name="features",
        accessor=MAAttrAccessor("features"),
        classes=[Feature],
        reference=feature_desc
    )
])

port_features_desc = port_desc[2]

feature_desc.setChildren([
    MAStringDescription(name="name", accessor=MAAttrAccessor("name"), required=True),
    MAStringDescription(name="value", accessor=MAAttrAccessor("value"), required=True)
])

descriptions = [host_desc, port_desc, feature_desc]

registry = registrator.register(*descriptions)


if __name__ == '__main__':

    host = Host()
    port = Port()
    feature = Feature()

    host.ip = "192.168.0.3"
    port.numofport = 81

    feature.name = "feature_0"
    feature.value = "value_0"

    port.features.append(feature)

    # when ORM mapping is performed one of the following two lines should be commented out (due to backpopulates)
    port.host = host
    # host.ports.append(port)

    serialized_str_host = MAReferencedDataHumanReadableSerializer().serializeHumanReadable(host, host_desc)
    logger.debug(f"Serialized host: {serialized_str_host}")
    dto_host = MAReferencedDataHumanReadableDeserializer().deserializeHumanReadable(serialized_str_host, host_desc)
    logger.debug(f"isinstance(dto_host, Host): {isinstance(dto_host, Host)}")
    logger.debug(f"host.ip: {host.ip}")
    logger.debug(f"dto_host.ip: {dto_host.ip}")
    logger.debug(f"host.ports[0].numofport: {host.ports[0].numofport}")
    logger.debug(f"dto_host.ports[0].numofport: {dto_host.ports[0].numofport}")
    logger.debug(f"host.ports[0].features[0].name: {host.ports[0].features[0].name}")
    logger.debug(f"dto_host.ports[0].features[0].name: {dto_host.ports[0].features[0].name}") # fails here
