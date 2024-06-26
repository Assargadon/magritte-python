import logging
import os
from unittest import TestCase

from sqlalchemy import create_engine

from Magritte.MAModel_class import MAModel
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

# engine = create_engine("sqlite://", echo=True)
conn_str = f"{os.getenv('CONN_STR_BASE', 'postgresql://postgres:secret@localhost')}/serializer_orm_test"
engine = create_engine(conn_str, echo=True)

registry.metadata.create_all(engine)


class MAReferencedDataWriterReaderVisitorPassthroughTest(TestCase):

    def setUp(self):
        self.serializer = MAReferencedDataHumanReadableSerializer()
        self.deserializer = MAReferencedDataHumanReadableDeserializer()

        self.host = Host()
        self.ports = [Port() for _ in range(2)]
        self.features = [Feature() for _ in range(3)]

        for i, feature in enumerate(self.features):
            feature.name = f"feature_{i}"
            feature.value = f"value_{i}"

        self.ports[0].host = self.host
        self.ports[0].numofport = 80
        self.ports[0].features = [self.features[0]]
        self.ports[1].host = self.host
        self.ports[1].numofport = 443
        self.ports[1].features = [self.features[1], self.features[2]]

        self.port = self.ports[0]

        self.host.ip = "192.168.0.1"
        # self.host.ports = self.ports

    def test_passthroughWithPort(self):
        serialized_str_port = self.serializer.serializeHumanReadable(self.port, port_desc)
        logger.debug(f"Serialized port: {serialized_str_port}")
        dto_port = self.deserializer.deserializeHumanReadable(serialized_str_port, port_desc)
        self.assertIsInstance(dto_port, Port, f"Passed through port should result in Port instance, got {dto_port}")
        self.assertEqual(self.port.numofport, dto_port.numofport, f"Passed through port should have the same numofport {self.port.numofport}, got {dto_port.numofport}")
        self.assertEqual(self.port.host.ip, dto_port.host.ip, f"Passed through port should have the same ip of the host {self.port.host.ip}, got {dto_port.host.ip}")
        self.assertEqual(len(self.port.host.ports), len(dto_port.host.ports), f"Passed through port should have the same number of ports of the host {len(self.port.host.ports)}, got {len(dto_port.host.ports)}")
        source_features = {feature.name: feature.value for feature in self.port.features}
        target_features = {feature.name: feature.value for feature in dto_port.features}
        self.assertDictEqual(
            source_features, target_features,
            f"Passed through port should have the same features of the port {source_features}, got {target_features}"
            )

    def test_passthroughWithHost(self):
        serialized_str_host = self.serializer.serializeHumanReadable(self.host, host_desc)
        logger.debug(f"Serialized host: {serialized_str_host}")
        dto_host = self.deserializer.deserializeHumanReadable(serialized_str_host, host_desc)
        self.assertIsInstance(dto_host, Host, f"Passed through host should result in Host instance, got {dto_host}")
        self.assertEqual(self.host.ip, dto_host.ip, f"Passed through host should have the same ip of the host {self.host.ip}, got {dto_host.ip}")
        self.assertEqual(len(self.host.ports), len(dto_host.ports), f"Passed through host should have the same number of ports of the host {len(self.host.ports)}, got {len(dto_host.ports)}")
        source_features = {feature.name: feature.value for port in self.host.ports for feature in port.features}
        target_features = {feature.name: feature.value for port in dto_host.ports for feature in port.features}
        self.assertDictEqual(source_features, target_features, f"Passed through host should have the same features of the host {source_features}, got {target_features}")


class RootCauseIsolationTest(TestCase):

    def test_serialize_deserialize_host(self):
        host = Host()
        port = Port()
        feature = Feature()

        host.ip = "192.168.0.3"
        port.host = host
        port.numofport = 81

        feature.name = "feature_0"
        feature.value = "value_0"

        port.features.append(feature)
        # host.ports.append(port)

        serialized_str_host = MAReferencedDataHumanReadableSerializer().serializeHumanReadable(host, host_desc)
        logger.debug(f"Serialized host: {serialized_str_host}")
        dto_host = MAReferencedDataHumanReadableDeserializer().deserializeHumanReadable(serialized_str_host, host_desc)
        self.assertIsInstance(dto_host, Host, f"Passed through host should result in Host instance, got {dto_host}")
        self.assertEqual(host.ip, dto_host.ip, f"Passed through host should have the same ip of the host {host.ip}, got {dto_host.ip}")
        self.assertEqual(len(host.ports), len(dto_host.ports), f"Passed through host should have the same number of ports of the host {len(host.ports)}, got {len(dto_host.ports)}")
        self.assertEqual(len(host.ports[0].features), len(dto_host.ports[0].features), f"Passed through host should have the same number of features of the port {len(host.ports[0].features)}, got {len(dto_host.ports[0].features)}")
        self.assertEqual(host.ports[0].features[0].name, dto_host.ports[0].features[0].name, f"Passed through host should have the same name of the feature {host.ports[0].features[0].name}, got {dto_host.ports[0].features[0].name}")
        self.assertEqual(host.ports[0].features[0].value, dto_host.ports[0].features[0].value, f"Passed through host should have the same value of the feature {host.ports[0].features[0].value}, got {dto_host.ports[0].features[0].value}")

    def test_serialize_deserialize_port(self):
        host = Host()
        port = Port()
        feature = Feature()

        host.ip = "192.168.0.4"
        port.host = host
        port.numofport = 81

        feature.name = "feature_0"
        feature.value = "value_0"

        port.features.append(feature)
        # host.ports.append(port)

        serialized_str_port = MAReferencedDataHumanReadableSerializer().serializeHumanReadable(port, port_desc)
        logger.debug(f"Serialized port: {serialized_str_port}")
        dto_port = MAReferencedDataHumanReadableDeserializer().deserializeHumanReadable(serialized_str_port, port_desc)
        self.assertIsInstance(dto_port, Port, f"Passed through port should result in Port instance, got {dto_port}")
        self.assertEqual(port.numofport, dto_port.numofport, f"Passed through port should have the same numofport {port.numofport}, got {dto_port.numofport}")
        self.assertEqual(port.host.ip, dto_port.host.ip, f"Passed through port should have the same ip of the host {port.host.ip}, got {dto_port.host.ip}")
        self.assertEqual(len(port.features), len(dto_port.features), f"Passed through port should have the same number of features of the port {len(port.features)}, got {len(dto_port.features)}")
        self.assertEqual(port.features[0].name, dto_port.features[0].name, f"Passed through port should have the same name of the feature {port.features[0].name}, got {dto_port.features[0].name}")
        self.assertEqual(port.features[0].value, dto_port.features[0].value, f"Passed through port should have the same value of the feature {port.features[0].value}, got {dto_port.features[0].value}")

