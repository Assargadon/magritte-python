from unittest import TestCase
from json import dumps, loads

from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer

from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port, Account


class MAReferencedDataWriterVisitorTestBase(TestCase):
    def setUp(self):
        provider = TestEnvironmentProvider()
        self.host = provider.hosts[0]
        self.hostDescription = TestModelDescriptor.description_for(Host.__name__)
        self.port = self.host.ports[5]
        self.portDescription = TestModelDescriptor.description_for(Port.__name__)
        self.account = provider.accounts[1]
        self.accountDescription = TestModelDescriptor.description_for(Account.__name__)

    def findDescriptionByProperty(self, prop):
        getter = prop.fget
        name = getter.__name__
        class_name = getter.__qualname__.split(".")[0]
        container = TestModelDescriptor.description_for(class_name)
        self.assertIsNotNone(container)
        descriptor = next(filter(lambda description: description.name == name, container.children), None)
        self.assertIsNotNone(descriptor)
        return descriptor


class MAReferencedDataWriterVisitorTest(MAReferencedDataWriterVisitorTestBase):

    def setUp(self):
        super().setUp()
        self.serializer = MAReferencedDataHumanReadableSerializer()

    def testStringDescription(self):
        hostIpDescription = self.findDescriptionByProperty(Host.ip)
        hostIpDumped = self.serializer.dumpHumanReadable(self.host.ip, hostIpDescription)
        self.assertEqual(hostIpDumped, self.host.ip, f"MAStringDescription in a dumped form should result in the same string {self.host.ip}, got {hostIpDumped}")
        hostIpSerialized = self.serializer.serializeHumanReadable(self.host.ip, hostIpDescription)
        hostIpJson = dumps(self.host.ip)
        self.assertEqual(hostIpSerialized, hostIpJson, f"MAStringDescription in a serialized form should result in a json encoded string {hostIpJson}, got {hostIpSerialized}")

    def testIntDescription(self):
        numofportDescription = self.findDescriptionByProperty(Port.numofport)
        numofportDumped = self.serializer.dumpHumanReadable(self.port.numofport, numofportDescription)
        self.assertEqual(numofportDumped, self.port.numofport, f"MAIntDescription in a dumped form should result in the same number {self.port.numofport}, got {numofportDumped}")
        numofportSerialized = self.serializer.serializeHumanReadable(self.port.numofport, numofportDescription)
        numofportJson = dumps(self.port.numofport)
        self.assertEqual(numofportSerialized, numofportJson, f"MAIntDescription in a serialized form should result in a json encoded number {numofportJson}, got {numofportSerialized}")

    def testElementDescriptionWithNone(self):
        ntlmDescription = self.findDescriptionByProperty(Account.ntlm)
        account = Account.random_account(self.port)
        account.ntlm = None
        ntlmDumped = self.serializer.dumpHumanReadable(account.ntlm, ntlmDescription)
        self.assertIsNone(ntlmDumped, f"MAElementDescription of None in a dumped form should result in None, got {ntlmDumped}")
        ntlmSerialized = self.serializer.serializeHumanReadable(account.ntlm, ntlmDescription)
        noneJson = dumps(None)
        self.assertEqual(ntlmSerialized,  noneJson, f"MAElementDescription of None in a serialized form should result in json null, got {ntlmSerialized}")

    def testToManyRelationDescription(self):
        portsDescription = self.findDescriptionByProperty(Host.ports)
        portsDumped = self.serializer.dumpHumanReadable(self.host.ports, portsDescription)
        self.assertIsInstance(portsDumped, list, f"MAToManyRelationDescription in a dumped form should result in a list, got {portsDumped}")
        portsSerialized = self.serializer.serializeHumanReadable(self.host.ports, portsDescription)
        portsFromJson = loads(portsSerialized)
        self.assertIsInstance(portsFromJson, list, "MAToManyRelationDescription in a serialized form should result in a json array")
        self.assertEqual(len(portsFromJson), len(self.host.ports), "MAToManyRelationDescription in a serialized form should be json array of the same length as original list")

    def testContainerDescription(self):
        hostDumped = self.serializer.dumpHumanReadable(self.host, self.hostDescription)
        self.assertIsInstance(hostDumped, dict, f"MAContainerDescription in a dumped form should result in a dict, got {hostDumped}")
        self.assertIn('_key', hostDumped, "MAContainerDescription in a dumped form should have internal '_key' property")
        for child in self.hostDescription.children:
            name = child.name
            self.assertIn(name, hostDumped, f"MAContainerDescription in a dumped form should have every child property, but {name} was not found")
        hostSerialized = self.serializer.serializeHumanReadable(self.host, self.hostDescription)
        hostFromJson = loads(hostSerialized)
        self.assertIsInstance(hostFromJson, dict, "MAContainerDescription in a serialized form should result in a json object")


class MAReferencedDataReaderVisitorTest(MAReferencedDataWriterVisitorTestBase):

    def setUp(self):
        super().setUp()
        self.deserializer = MAReferencedDataHumanReadableDeserializer()

    def testStringDescription(self):
        hostIpDescription = self.findDescriptionByProperty(Host.ip)
        hostIpJson = dumps(self.host.ip)
        hostIpDeserialized = self.deserializer.deserializeHumanReadable(hostIpJson, hostIpDescription)
        self.assertEqual(hostIpDeserialized, self.host.ip, f"MAStringDescription in a deserialized form should result in the same string {self.host.ip}, got {hostIpDeserialized}")

    def testIntDescription(self):
        numofportDescription = self.findDescriptionByProperty(Port.numofport)
        numofportJson = dumps(self.port.numofport)
        numofportDeserialized = self.deserializer.deserializeHumanReadable(numofportJson, numofportDescription)
        self.assertEqual(numofportDeserialized, self.port.numofport, f"MAIntDescription in a deserialized form should result in the same number {self.port.numofport}, got {numofportDeserialized}")

    def testElementDescriptionWithNone(self):
        ntlmDescription = self.findDescriptionByProperty(Account.ntlm)
        noneJson = dumps(None)
        ntlmDeserialized = self.deserializer.deserializeHumanReadable(noneJson, ntlmDescription)
        self.assertIsNone(ntlmDeserialized, f"MAElementDescription of None in a deserialized form should result in None, got {ntlmDeserialized}")

    def testToManyRelationDescription(self):
        portsDescription = self.findDescriptionByProperty(Host.ports)
        portsJson = dumps([])
        portsDeserialized = self.deserializer.deserializeHumanReadable(portsJson, portsDescription)
        self.assertIsInstance(portsDeserialized, list, f"MAToManyRelationDescription in a deserialized form should result in a list, got {portsDeserialized}")


class MAReferencedDataWriterReaderVisitorPassthroughTest(MAReferencedDataWriterVisitorTestBase):

    def setUp(self):
        super().setUp()
        self.serializer = MAReferencedDataHumanReadableSerializer()
        self.deserializer = MAReferencedDataHumanReadableDeserializer()

    def test_passthroughWithPort(self):
        serialized_str_port = self.serializer.serializeHumanReadable(self.port, self.portDescription)
        dto_port = self.deserializer.deserializeHumanReadable(serialized_str_port, self.portDescription)
        self.assertIsInstance(dto_port, Port, f"Passed through port should result in Port instance, got {dto_port}")
        self.assertEqual(self.port.numofport, dto_port.numofport, f"Passed through port should have the same numofport {self.port.numofport}, got {dto_port.numofport}")
        self.assertEqual(self.port.host.ip, dto_port.host.ip, f"Passed through port should have the same ip of the host {self.port.host.ip}, got {dto_port.host.ip}")
        self.assertEqual(len(self.port.host.ports), len(dto_port.host.ports), f"Passed through port should have the same number of ports of the host {len(self.port.host.ports)}, got {len(dto_port.host.ports)}")

    def test_passthroughWithHost(self):
        serialized_str_host = self.serializer.serializeHumanReadable(self.host, self.hostDescription)
        dto_host = self.deserializer.deserializeHumanReadable(serialized_str_host, self.hostDescription)
        self.assertIsInstance(dto_host, Host, f"Passed through host should result in Host instance, got {dto_host}")
        self.assertEqual(self.host.ip, dto_host.ip, f"Passed through host should have the same ip of the host {self.host.ip}, got {dto_host.ip}")
        self.assertEqual(len(self.host.ports), len(dto_host.ports), f"Passed through host should have the same number of ports of the host {len(self.host.ports)}, got {len(dto_host.ports)}")

    def test_passthroughWithPorts(self):
        portsDescription = self.findDescriptionByProperty(Host.ports)
        serialized_str_ports = self.serializer.serializeHumanReadable(self.host.ports, portsDescription)
        dto_ports = self.deserializer.deserializeHumanReadable(serialized_str_ports, portsDescription)
        self.assertIsInstance(dto_ports, list, f"Passed through ports should result in list instance, got {dto_ports}")
        self.assertEqual(len(self.host.ports), len(dto_ports), f"Passed through ports list should have the same length as for host {len(self.host.ports)}, got {len(dto_ports)}")

