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


host_desc = MAContainer(kind=Host, name="Host")
port_desc = MAContainer(kind=Port, name="Port")

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
])

descriptions = [host_desc, port_desc]

registry = registrator.register(*descriptions)


if __name__ == '__main__':

    host = Host()
    port = Port()

    host.ip = "192.168.0.3"
    port.numofport = 81

    # when ORM mapping is performed one of the following two lines should be commented out (due to backpopulates)
    port.host = host
    # host.ports.append(port)

    serialized_str_port = MAReferencedDataHumanReadableSerializer().serializeHumanReadable(port, port_desc)
    logger.debug(f"Serialized port: {serialized_str_port}")
    dto_port = MAReferencedDataHumanReadableDeserializer().deserializeHumanReadable(serialized_str_port, port_desc)
    logger.debug(f"isinstance(dto_port, Port): {isinstance(dto_port, Port)}")
    logger.debug(f"port.host.ip: {port.host.ip}")
    logger.debug(f"dto_port.host.ip: {dto_port.host.ip}")
    logger.debug(f"port.numofport: {port.numofport}")
    logger.debug(f"dto_port.numofport: {dto_port.numofport}")
    logger.debug(f"port.host.ports: {port.host.ports}")
    logger.debug(f"dto_port.host.ports: {dto_port.host.ports}")
