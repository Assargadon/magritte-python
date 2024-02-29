from unittest import TestCase
from json import dumps, loads
from datetime import datetime, timedelta, date, time

from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
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
        hostIpDumped = self.serializer.dumpHumanReadable(self.host, hostIpDescription)
        self.assertEqual(hostIpDumped, self.host.ip, f"MAStringDescription in a dumped form should result in the same string {self.host.ip}, got {hostIpDumped}")
        hostIpSerialized = self.serializer.serializeHumanReadable(self.host, hostIpDescription)
        hostIpJson = dumps(self.host.ip)
        self.assertEqual(hostIpSerialized, hostIpJson, f"MAStringDescription in a serialized form should result in a json encoded string {hostIpJson}, got {hostIpSerialized}")

    def testIntDescription(self):
        numofportDescription = self.findDescriptionByProperty(Port.numofport)
        numofportDumped = self.serializer.dumpHumanReadable(self.port, numofportDescription)
        self.assertEqual(numofportDumped, self.port.numofport, f"MAIntDescription in a dumped form should result in the same number {self.port.numofport}, got {numofportDumped}")
        numofportSerialized = self.serializer.serializeHumanReadable(self.port, numofportDescription)
        numofportJson = dumps(self.port.numofport)
        self.assertEqual(numofportSerialized, numofportJson, f"MAIntDescription in a serialized form should result in a json encoded number {numofportJson}, got {numofportSerialized}")

    def testElementDescriptionWithNone(self):
        ntlmDescription = self.findDescriptionByProperty(Account.ntlm)
        account = Account.random_account(self.port)
        account.ntlm = None
        ntlmDumped = self.serializer.dumpHumanReadable(account, ntlmDescription)
        self.assertIsNone(ntlmDumped, f"MAElementDescription of None in a dumped form should result in None, got {ntlmDumped}")
        ntlmSerialized = self.serializer.serializeHumanReadable(account, ntlmDescription)
        noneJson = dumps(None)
        self.assertEqual(ntlmSerialized,  noneJson, f"MAElementDescription of None in a serialized form should result in json null, got {ntlmSerialized}")

    def testToManyRelationDescription(self):
        portsDescription = self.findDescriptionByProperty(Host.ports)
        portsDumped = self.serializer.dumpHumanReadable(self.host, portsDescription)
        self.assertIsInstance(portsDumped, list, f"MAToManyRelationDescription in a dumped form should result in a list, got {portsDumped}")
        portsSerialized = self.serializer.serializeHumanReadable(self.host, portsDescription)
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


class MAReferencedDataWriterReaderVisitorTest(MAReferencedDataWriterVisitorTestBase):

    def setUp(self):
        super().setUp()
        self.serializer = MAReferencedDataHumanReadableSerializer()
        self.deserializer = MAReferencedDataHumanReadableDeserializer()
