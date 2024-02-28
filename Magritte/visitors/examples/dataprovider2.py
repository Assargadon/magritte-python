from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.accessors.MADictAccessor_class import MADictAccessor

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription

from Magritte.visitors.MAReferencedDataWriterReader_visitors import (
    MAReferencedDataHumanReadableSerializer,
    MAReferencedDataHumanReadableDeserializer,
    )

from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port


class Dictionary:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description


class MisconfigurationType(Dictionary):
    def __init__(self, code, name, description=None):
        super().__init__(name, description)
        self.code = code


misconfigurationType_desc = MAContainer(kind=MisconfigurationType, name="MisconfigurationType")
misconfigurationType_desc += MAStringDescription(accessor=MAAttrAccessor("code"), required=True)
misconfigurationType_desc += MAStringDescription(accessor=MAAttrAccessor("name"), required=True)
misconfigurationType_desc += MAStringDescription(accessor=MAAttrAccessor("description"), required=False)


class ServiceType(Dictionary):
    def __init__(self, name, description=None, possible_misconfigurations=None):
        super().__init__(name, description)
        self.possible_misconfigurations = possible_misconfigurations if possible_misconfigurations else []

    @staticmethod
    def named(name):
        for st in ServiceType.entries:
            if st.name == name:
                return st
        return None

    @staticmethod
    def misconfigurations(service_name, misconfiguration_code):
        st = ServiceType.named(service_name)
        if st is not None:
            for mc in st.possible_misconfigurations:
                if mc.code == misconfiguration_code:
                    return mc
        return None


ServiceType.entries = [
    ServiceType(
        "ssh",
        possible_misconfigurations=[
            MisconfigurationType("notimeout", "immediate password re-request"),
            MisconfigurationType("root", "login as root possible"),
            ]
        ),
    ServiceType(
        "https",
        possible_misconfigurations=[
            MisconfigurationType("acac", "Access-Control-Allow-Credentials set to true"),
            ]
        ),
    ServiceType(
        "ldap",
        possible_misconfigurations=[
            MisconfigurationType("alae", "Anonymous LDAP access enabled"),
            ]
        ),
    ServiceType(
        "smb",
        possible_misconfigurations=[
            MisconfigurationType("ssne", "SMB Signing not enforced"),
            ]
        ),
    ]


serviceType_desc = MAContainer(kind=ServiceType, name="ServiceType")
serviceType_desc += MAStringDescription(accessor=MAAttrAccessor("name"), required=True)
serviceType_desc += MAStringDescription(accessor=MAAttrAccessor("description"), required=False)
serviceType_desc += MAToManyRelationDescription(
    reference=misconfigurationType_desc,
    accessor=MAAttrAccessor("possible_misconfigurations")
    )


class Port:
    def __init__(self, host, number, service_type, misconfigurations=None):
        self.host = host
        self.number = number
        self.service_type = service_type
        self.misconfigurations = misconfigurations if misconfigurations else []


port_desc = MAContainer(kind=Port, name="Port")
port_desc += MAToOneRelationDescription(
    reference=TestModelDescriptor.description_for("Host"),
    accessor=MAAttrAccessor("host"),
    required=True
    )
port_desc += MAStringDescription(accessor=MAAttrAccessor("number"), required=True)
port_desc += MAToOneRelationDescription(
    reference=serviceType_desc,
    accessor=MAAttrAccessor("service_type")
    )
port_desc += MAToManyRelationDescription(
    reference=misconfigurationType_desc,
    accessor=MAAttrAccessor("misconfigurations")
    )


class IP4:
    def __init__(self, addr, ports=None):
        self.addr = addr
        self.ports = ports if ports else []

    def add_port(self, number, service_type):
        self.ports.append(Port(self, number, service_type))
        return self

    # searches for the Port object and, if found, adds the misconfiguration to it
    def add_misconfiguration(self, port, misconfiguration):
        for p in self.ports:
            if p.number == port:
                p.misconfigurations.append(misconfiguration)
                # print(f"Added `{misconfiguration.name}` to port `{p.number}` on host `{self.addr}`")
        return self


IP4_desc = MAContainer(kind=IP4, name="IP4")
IP4_desc += MAStringDescription(accessor=MAAttrAccessor("addr"), required=True)
IP4_desc += MAToManyRelationDescription(
    reference=port_desc,
    accessor=MAAttrAccessor("ports"),
    required=True
    )

# ============== DEMO ENVIRONMENT DATA==============
demo_env = {
    "dictionaries": {
        "service_types": ServiceType.entries
        },
    "hosts": [
        IP4('192.168.0.1')
        .add_port("80", ServiceType.named("https"))
        .add_misconfiguration("80", ServiceType.misconfigurations("https", "acac"))

        .add_port("22", ServiceType.named("ssh"))
        .add_misconfiguration("22", ServiceType.misconfigurations("ssh", "root"))
        ]
    }
# ============== /DEMO ENVIRONMENT DATA==============

demo_env_desc = MAContainer(name="DemoEnvironment")
dictionaries_desc = MAContainer()
dictionaries_desc += MAToManyRelationDescription(
    reference=serviceType_desc,
    accessor=MADictAccessor("service_types")
    )

demo_env_desc += MAToOneRelationDescription(
    accessor=MADictAccessor("dictionaries"),
    reference=dictionaries_desc
    )

demo_env_desc += MAToManyRelationDescription(
    name="hosts",
    reference=IP4_desc,
    accessor=MADictAccessor("hosts")
    )

if __name__ == "__main__":
    serializer = MAReferencedDataHumanReadableSerializer()

    json_str = serializer.serializeHumanReadable(demo_env, demo_env_desc)
    print(json_str)
