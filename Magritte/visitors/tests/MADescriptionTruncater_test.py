from unittest import TestCase

from PIL.TiffImagePlugin import SOFTWARE

from Magritte.visitors.MADescriptionTruncater_visitors import MADescriptionTruncater

from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableSerializer, \
    MAReferencedDataHumanReadableDeserializer
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider, Host, Port, Account, User, \
    SoftwarePackage


class MADescriptionTruncaterTest(TestCase):
    def setUp(self):
        descriptors = TestModelDescriptorProvider()
        provider = TestEnvironmentProvider()
        self.truncater = MADescriptionTruncater()
        self.serializer = MAReferencedDataHumanReadableSerializer()
        self.deserializer = MAReferencedDataHumanReadableDeserializer()
        self.host = provider.hosts[0]
        self.hostDescription = descriptors.description_for(Host.__name__)
        self.port = self.host.ports[5]
        self.portDescription = descriptors.description_for(Port.__name__)
        self.account = provider.accounts[1]
        self.accountDescription = descriptors.description_for(Account.__name__)
        self.user = provider.users[1]
        self.userDescription = descriptors.description_for(User.__name__)

    def _performPasstrough(self, model, description, pathes_whitelist):
        description_truncated = self.truncater.truncate(
            description,
            pathes_whitelist,
        )
        serialized = self.serializer.serializeHumanReadable(model, description_truncated)
        model_passtrough = self.deserializer.deserializeHumanReadable(serialized, description)
        return model_passtrough

    def _compareHostsPorts(self, host, host_passtrough):
        self.assertEqual(len(host_passtrough.ports), len(host.ports), 'Passtrough model ports should have the same number of entries')
        for i in range(len(host_passtrough.ports)):
            port = host.ports[i]
            port_passtrough = host_passtrough.ports[i]
            self.assertEqual(port_passtrough.numofport, port.numofport, 'Passtrough model ports entries should have the same numofport')
            self.assertIsInstance(port_passtrough, Port, 'Passtrough model ports entries should have kind Port')

    def _compareHostsSoftware(self, host, host_passtrough):
        self.assertEqual(len(host_passtrough.software), len(host.software), 'Passtrough model software should have the same number of entries')
        for i in range(len(host_passtrough.software)):
            software = host.software[i]
            software_passtrough = host_passtrough.software[i]
            self.assertEqual(software_passtrough.name, software.name, 'Passtrough model ports entries should have the same name')
            self.assertIsInstance(software_passtrough, SoftwarePackage, 'Passtrough model software entries should have kind SoftwarePackage')

    def testHostEmptyWhitelist(self):
        model = self.host
        description = self.hostDescription
        pathes_whitelist = []
        model_passtrough = self._performPasstrough(model, description, pathes_whitelist)
        self.assertIsInstance(model_passtrough, model.__class__, f'Passtrough model should be of the same kind {model.__class__}')
        self.assertEqual(len(model_passtrough.ports), 0, 'Passtrough model should have ports not set')
        self.assertEqual(len(model_passtrough.software), 0, 'Passtrough model should have software not set')

    def testHostPortsWhitelist(self):
        model = self.host
        description = self.hostDescription
        pathes_whitelist = [
            '.ports',
        ]
        model_passtrough = self._performPasstrough(model, description, pathes_whitelist)
        self.assertIsInstance(model_passtrough, model.__class__, f'Passtrough model should be of the same kind {model.__class__}')
        self._compareHostsPorts(model, model_passtrough)
        for port_passtrough in model_passtrough.ports:
            self.assertIsNone(port_passtrough.host, 'Passtrough model ports entries should have host not set')
        self.assertEqual(len(model_passtrough.software), 0, 'Passtrough model should have software not set')

    def testHostPortsHostWhitelist(self):
        model = self.host
        description = self.hostDescription
        pathes_whitelist = [
            '.ports.host',
        ]
        model_passtrough = self._performPasstrough(model, description, pathes_whitelist)
        self.assertIsInstance(model_passtrough, model.__class__, f'Passtrough model should be of the same kind {model.__class__}')
        self._compareHostsPorts(model, model_passtrough)
        for port_passtrough in model_passtrough.ports:
            self.assertEqual(port_passtrough.host, model_passtrough, 'Passtrough model ports entries should have host set')
        model_passtrough_ports_host = model_passtrough.ports[0].host
        self.assertEqual(len(model_passtrough_ports_host.ports), len(model_passtrough.ports), 'Passtrough model ports should have the same number of entries')
        self.assertEqual(len(model_passtrough.software), 0, 'Passtrough model should have software not set')

    def testHostPortsSoftwareWhitelist(self):
        model = self.host
        description = self.hostDescription
        pathes_whitelist = [
            '.ports',
            '.software',
        ]
        model_passtrough = self._performPasstrough(model, description, pathes_whitelist)
        self.assertIsInstance(model_passtrough, model.__class__, f'Passtrough model should be of the same kind {model.__class__}')
        self._compareHostsPorts(model, model_passtrough)
        for port_passtrough in model_passtrough.ports:
            self.assertIsNone(port_passtrough.host, 'Passtrough host.ports entries should have host not set')
        self._compareHostsSoftware(model, model_passtrough)
