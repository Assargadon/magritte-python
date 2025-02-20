import logging
from copy import copy
from unittest import TestCase
from json import dumps, loads

from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.model_for_tests import SoftwarePackage
# from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableSerializer
# from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableDeserializer
from Magritte.visitors.MAReaderWriterWalkerVisitors import MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer

from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider, Host, Port, Account, User, Organization, SubscriptionPlan


class MAReferencedDataWriterVisitorTestBase(TestCase):
    def setUp(self):
        provider = TestEnvironmentProvider()
        self.descriptors = TestModelDescriptorProvider()
        self.host = provider.hosts[0]
        self.hostDescription = self.descriptors.description_for(Host.__name__)
        self.port = self.host.ports[5]
        self.portDescription = self.descriptors.description_for(Port.__name__)
        self.account = provider.accounts[1]
        self.accountDescription = self.descriptors.description_for(Account.__name__)
        self.user = provider.users[1]
        self.userDescription = self.descriptors.description_for(User.__name__)
        self.software = provider.hosts[0].software[0]
        self.softwareDescription = self.descriptors.description_for(SoftwarePackage.__name__)
        self.subscriptionPlan = provider.subscription_plans[1]
        self.subscriptionPlanDescription = self.descriptors.description_for(SubscriptionPlan.__name__)
        self.accountWithoutNTLM = provider.accounts[0]
        self.assertIsNone(self.accountDescription['ntlm'].undefinedValue)
        self.accountWithoutNTLM.ntlm = self.accountDescription['ntlm'].undefinedValue
        self.subscriptionPlanWithoutPrice = provider.subscription_plans[0]
        self.subscriptionPlanWithoutPrice.price = self.subscriptionPlanDescription['price'].undefinedValue

    def findDescription(self, class_name, name):
        container = self.descriptors.description_for(class_name)
        self.assertIsNotNone(container)
        descriptor = container[name]
        self.assertIsNotNone(descriptor)
        res_desc = copy(descriptor)
        res_desc.accessor = MAIdentityAccessor()
        return res_desc

    def findDescriptionByName(self, cls, name):
        class_name = cls.__name__
        return self.findDescription(class_name, name)

    def findDescriptionByProperty(self, prop):
        getter = prop.fget
        name = getter.__name__
        class_name = getter.__qualname__.split(".")[0]
        return self.findDescription(class_name, name)


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

    def testToOneRelationDescription(self):
        organizationDescription = self.findDescriptionByProperty(User.organization)
        organizationDumped = self.serializer.dumpHumanReadable(self.user.organization, organizationDescription)
        self.assertIsInstance(organizationDumped, dict, f"MAToOneRelationDescription in a dumped form should result in a dict, got {organizationDumped}")
        organizationSerialized = self.serializer.serializeHumanReadable(self.user.organization, organizationDescription)
        organizationFromJson = loads(organizationSerialized)
        self.assertIsInstance(organizationFromJson, dict, "MAToOneRelationDescription in a serialized form should result in a json object")

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
        self.assertIn('-x-magritte-key', hostDumped, "MAContainerDescription in a dumped form should have internal '-x-magritte-key' property")
        for child in self.hostDescription.children:
            name = child.name
            self.assertIn(name, hostDumped, f"MAContainerDescription in a dumped form should have every child property, but {name} was not found")
        hostSerialized = self.serializer.serializeHumanReadable(self.host, self.hostDescription)
        hostFromJson = loads(hostSerialized)
        self.assertIsInstance(hostFromJson, dict, "MAContainerDescription in a serialized form should result in a json object")

    def testSingleOptionDescriptionToElementDescription(self):
        portStatusDescription = self.findDescriptionByProperty(Port.status)
        portStatusDumped = self.serializer.dumpHumanReadable(self.port.status, portStatusDescription)
        self.assertIsInstance(portStatusDumped, str, f"MASingleOptionDecription of MAStringDescription in a dumped form should result in a str, got {portStatusDumped}")
        self.assertEqual(self.port.status, portStatusDumped, "MASingleOptionDecription of MAStringDescription in a dumped form should be equal to the source string")

    def testSingleOptionDescriptionToContainerDescription(self):
        userPlanDescription = self.findDescriptionByName(User, 'plan')
        userPlanDumped = self.serializer.dumpHumanReadable(self.user.plan, userPlanDescription)
        self.assertIsInstance(userPlanDumped, dict, f"MASingleOptionDecription of MAContainer in a dumped form should result in a dict, got {userPlanDumped}")
        self.assertEqual(userPlanDumped['name'], self.user.plan.name, f"MASingleOptionDecription of MAContainer in a dumped form should have properties from the referenced object")
        self.assertEqual(userPlanDumped['price'], self.user.plan.price, f"MASingleOptionDecription of MAContainer in a dumped form should have properties from the referenced object")

    def testIgnoreInvisible(self):
        softwareCodeDescription = self.findDescriptionByName(SoftwarePackage, 'code')
        self.assertFalse(softwareCodeDescription.isVisible(), "Initial condition is not met. 'code' property should be invisible")
        softwareDumped = self.serializer.dumpHumanReadable(self.host.software[0], self.softwareDescription)
        self.assertNotIn(softwareCodeDescription.name, softwareDumped, "Invisible properties should not be included in the dumped form")

    def testSkipDefaultUndefinedValue(self):
        accountWithoutNTLMDumped = self.serializer.dumpHumanReadable(self.accountWithoutNTLM, self.accountDescription)
        self.assertNotIn('ntlm', accountWithoutNTLMDumped, "Properties with default undefined value should not be included in the dumped form")

    def testSkipCustomUndefinedValue(self):
        subscriptionPlanWithoutPriceDumped = self.serializer.dumpHumanReadable(self.subscriptionPlanWithoutPrice, self.subscriptionPlanDescription)
        self.assertNotIn('price', subscriptionPlanWithoutPriceDumped, "Properties with custom undefined value should not be included in the dumped form")

    def testDistinctKeys(self):
        allKeys = set()
        def traverseList(l):
            for val in l:
                if isinstance(val, dict):
                    traverseDict(val)
                if isinstance(val, list):
                    traverseList(val)
        def traverseDict(d):
            for key in d:
                val = d[key]
                if key == '-x-magritte-key':
                    self.assertNotIn(val, allKeys, "MAContainerDescription in a dumped form should not have duplicated '-x-magritte-key' values at any depth")
                    allKeys.add(val)
                if isinstance(val, dict):
                    traverseDict(val)
                if isinstance(val, list):
                    traverseList(val)
        hostDumped = self.serializer.dumpHumanReadable(self.host, self.hostDescription)
        self.assertIsInstance(hostDumped, dict, f"MAContainerDescription in a dumped form should result in a dict, got {hostDumped}")
        traverseDict(hostDumped)
        self.assertGreater(len(allKeys), 1, f"MAContainerDescription with child containers in a dumped form should have '-x-magritte-key' properties at several depths")



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

    def testToOneRelationDescription(self):
        hostDescription = self.findDescriptionByProperty(Port.host)
        hostJson = '{"-x-magritte-key": 1, "ip": "192.168.0.1", "ports": []}'
        hostDeserialized = self.deserializer.deserializeHumanReadable(hostJson, hostDescription)
        self.assertIsInstance(hostDeserialized, Host, f"MAToOneRelationDescription in a deserialized form should result in a Host instance, got {hostDeserialized}")

    def testToManyRelationDescription(self):
        portsDescription = self.findDescriptionByProperty(Host.ports)
        portsJson = dumps([])
        portsDeserialized = self.deserializer.deserializeHumanReadable(portsJson, portsDescription)
        self.assertIsInstance(portsDeserialized, list, f"MAToManyRelationDescription in a deserialized form should result in a list, got {portsDeserialized}")

    def testSingleOptionDescriptionToElementDescription(self):
        portStatusDescription = self.findDescriptionByProperty(Port.status)
        portStatusJson = dumps(self.port.status)
        portStatusDeserialized = self.deserializer.deserializeHumanReadable(portStatusJson, portStatusDescription)
        self.assertIsInstance(portStatusDeserialized, str, f"MASingleOptionDecription of MAStringDescription in a deserialized form should result in a str, got {portStatusDeserialized}")
        self.assertEqual(self.port.status, portStatusDeserialized, "MASingleOptionDecription of MAStringDescription in a deserialized form should be equal to the source string")

    def testIgnoreInvisible(self):
        softwareCodeDescription = self.findDescriptionByName(SoftwarePackage, 'code')
        self.assertFalse(softwareCodeDescription.isVisible(), "Initial condition is not met. 'code' property should be invisible")
        softwareJson = '{"-x-magritte-key": 1, "name": "Red Technology Database", "version": "1.2.3"}'
        softwareDeserialized = self.deserializer.deserializeHumanReadable(softwareJson, self.softwareDescription)
        self.assertEqual(softwareDeserialized.code, self.softwareDescription.undefinedValue, "Invisible properties should not be included in the deserialized form")

    def testSkipDefaultUndefinedValue(self):
        accountWithoutNTLMJson = '''
        {"-x-magritte-key": 1, "login": "john.doe", "password": "123", "reg_timestamp": "2020-01-01T00:00:00", "days": 30,
        "port": {"-x-magritte-key": 2, "portnum": 80, "status": "open",
        "host": {"-x-magritte-key": 3, "ip": "192.168.0.1", "ports": [2]}}}
        '''
        accountWithoutNTLMDeserialized = self.deserializer.deserializeHumanReadable(accountWithoutNTLMJson, self.accountDescription)
        self.assertEqual(accountWithoutNTLMDeserialized.ntlm, self.accountDescription['ntlm'].undefinedValue, "Properties with default undefined value should not be included in the deserialized form")

    def testSkipCustomUndefinedValue(self):
        subscriptionPlanWithoutPriceJson = '{"-x-magritte-key": 1, "name": "Free"}'
        subscriptionPlanWithoutPriceDeserialized = self.deserializer.deserializeHumanReadable(subscriptionPlanWithoutPriceJson, self.subscriptionPlanDescription)
        self.assertEqual(subscriptionPlanWithoutPriceDeserialized.price, self.subscriptionPlanDescription['price'].undefinedValue, "Properties absent from dumped form should be set to undefined value")


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
        self.assertEqual(self.port.status, dto_port.status, f"Passed through port should have the same status {self.port.status}, got {dto_port.status}")
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

    def test_passthroughWithUser(self):
        serialized_str_user = self.serializer.serializeHumanReadable(self.user, self.userDescription)
        dto_user = self.deserializer.deserializeHumanReadable(serialized_str_user, self.userDescription)
        self.assertIsInstance(dto_user, User, f"Passed through host should result in Host instance, got {dto_user}")
        self.assertIsInstance(dto_user.plan, SubscriptionPlan, f"Passed through user should have SubscriptionPlan instance in plan, got {dto_user.plan}")
        self.assertIsInstance(dto_user.organization, Organization, f"Passed through user should have Organization instance in organization, got {dto_user.organization}")
        self.assertEqual(self.user.regnum, dto_user.regnum, f"Passed through user should have the same regnum {self.user.regnum}, got {dto_user.regnum}")
        self.assertEqual(self.user.dateofbirth, dto_user.dateofbirth, f"Passed through user should have the same dateofbirth {self.user.dateofbirth}, got {dto_user.dateofbirth}")
        self.assertEqual(len(self.user.setofaccounts), len(dto_user.setofaccounts), f"Passed through user should have the same number of accounts {len(self.user.setofaccounts)}, got {len(dto_user.setofaccounts)}")
        self.assertEqual(len(self.user.organization.listusers), len(dto_user.organization.listusers), f"Passed through user should have the same number of users of the organization {len(self.user.organization.listusers)}, got {len(dto_user.organization.listusers)}")
