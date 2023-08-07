# ==================== For testing. ====================
from datetime import datetime

from MADateAndTimeDescription_class import MADateAndTimeDescription
from MAFloatDescription_class import MAFloatDescription
from MAIntDescription_class import MAIntDescription
from MAStringDescription_class import MAStringDescription
from MAIdentityAccessor_class import MAIdentityAccessor
from MARelationDescription_class import MARelationDescription
from MAAttrAccessor_class import MAAttrAccessor
from MAContainer_class import MAContainer
from Magritte.MAJsonWriter_visitors import MAValueJsonWriter, MAObjectJsonWriter
from Magritte.MAOptionDescription_class import MAOptionDescription


class TestObject1:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class TestObject2:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_object: TestObject1):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_object = ref_object


'''
# ==================== Domain-specific helper classes (for demo). ====================

class GlossaryDescriptor:
    @classmethod
    def description_for(cls, glossary_type: str) -> MAContainer:
        """Returns a description for the given glossary type."""

        desc_container = MAContainer()

        if glossary_type == 'Service':
            desc_container.setChildren([
                MAStringDescription(name='name', label='Name', required=True, accessor=MAAttrAccessor('name')),
                MAIntDescription(name='standard_port', label='Standard Port', accessor=MAAttrAccessor('standard_port')),
                ])

        elif glossary_type == 'ActionType':
            desc_container.setChildren([
                MAStringDescription(name='name', label='Name', required=True, accessor=MAAttrAccessor('name')),
                # !TODO: describe needed_facts_descriptor
                #  (as MAContainer with param_name(MAStringDescription) and param_type(MARelationDescription))
                # !TODO: describe key_result_fact_types
                #  (as MAToManyRelationDescription with FactType)
                # !TODO Change to MAToOneRelationDescription when it is available
                MARelationDescription(
                    name='needed_proxy_action',
                    label='Needed Proxy Action',
                    accessor=MAAttrAccessor('needed_proxy_action'),
                    ),
                ])
            # needed_proxy_action attribute references ActionType description (i.e. circular reference)
            desc_container[1].reference = desc_container

        else:
            desc_container.setChildren([
                MAStringDescription(name='name', label='Name', required=True, accessor=MAAttrAccessor('name')),
                ])

        return desc_container


class FactDescriptor:
    @classmethod
    def description_for(cls, fact_type: str) -> MAContainer:
        """Returns a description for the given glossary type."""

        desc_container = MAContainer()

        if fact_type == 'IP4':
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='address', label='IP Address', required=True, accessor=MAAttrAccessor('address')
                        ),
                    ]
                )

        elif fact_type == 'Port':
            desc_container.setChildren(
                [
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(
                        name='ip4_addr', label='IP Address', required=True, accessor=MAAttrAccessor('ip4_addr')
                        ),
                    MAIntDescription(
                        name='port_num', label='Port Number', required=True, accessor=MAAttrAccessor('port_num')
                        ),
                    MAOptionDescription(
                        name='service', label='Service', required=True, accessor=MAAttrAccessor('service')
                        ),
                    ]
                )
            # !TODO Change to reference initialization via constructor when it is available
            desc_container[0].reference = cls.description_for("IP4")
            desc_container[2].reference = GlossaryDescriptor.description_for("Service")

        elif fact_type == "IP4Scope":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='address', label='Network Address', required=True, accessor=MAAttrAccessor('address')
                        ),
                    MAIntDescription(name='mask', label='Mask', required=True, accessor=MAAttrAccessor('mask')),
                    ]
                )

        elif fact_type == "Me":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='interface', label='Interface Name', required=True, accessor=MAAttrAccessor('interface')
                        ),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(
                        name='ip4_addr', label='IP4 Address', required=True, accessor=MAAttrAccessor('ip4_addr')
                        ),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(name='net', label='Subnet', required=True, accessor=MAAttrAccessor('net')),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(name='gateway', label='Default Gateway', accessor=MAAttrAccessor('gateway')),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(name='DNS', label='DNS Server', accessor=MAAttrAccessor('DNS')),
                    ]
                )
            # !TODO Change to reference initialization via constructor when it is available
            desc_container[1].reference = cls.description_for("IP4")
            desc_container[2].reference = cls.description_for("IP4Scope")
            desc_container[3].reference = cls.description_for("IP4")
            desc_container[4].reference = cls.description_for("IP4")

        elif fact_type == "Poisoning":
            desc_container.setChildren(
                [
                    MAOptionDescription(
                        name='protocol', label='Poisoned Protocol', required=True, accessor=MAAttrAccessor('protocol')
                        ),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(
                        name='source', label='Source IP', required=True, accessor=MAAttrAccessor('source')
                        ),
                    MAStringDescription(
                        name='searched_name', label='Searched Name', required=True,
                        accessor=MAAttrAccessor('searched_name')
                        ),
                    MADateAndTimeDescription(
                        name='happened', label='Happened', required=True, accessor=MAAttrAccessor('happened')
                        ),
                    ]
                )
            # !TODO Change to reference initialization via constructor when it is available
            desc_container[0].reference = GlossaryDescriptor.description_for("Protocol")
            desc_container[1].reference = cls.description_for("IP4")

        elif fact_type == "IncomingSession":
            desc_container.setChildren(
                [
                    MAOptionDescription(
                        name='protocol', label='Application Protocol', required=True,
                        accessor=MAAttrAccessor('protocol')
                        ),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(
                        name='source', label='Source IP', required=True, accessor=MAAttrAccessor('source')
                        ),
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    MADateAndTimeDescription(
                        name='happened', label='Happened', required=True, accessor=MAAttrAccessor('happened')
                        ),
                    # Current Pydantic model uses int field reference. Should change to MAToOneRelation
                    # MARelationDescription(name='caused_by', label='Caused by', accessor=MAAttrAccessor('caused_by')),
                    MAIntDescription(name='caused_by', label='Caused by', accessor=MAAttrAccessor('caused_by'))
                    ]
                )
            # !TODO Change to reference initialization via constructor when it is available
            desc_container[0].reference = GlossaryDescriptor.description_for("Protocol")
            desc_container[1].reference = cls.description_for("IP4")

        elif fact_type == "RelayedSession":
            desc_container.setChildren(
                [
                    MAOptionDescription(
                        name='protocol', label='Application Protocol', required=True,
                        accessor=MAAttrAccessor('protocol')
                        ),
                    # !TODO Change to MAToOneRelationDescription when it is available
                    MARelationDescription(
                        name='destination', label='Destination IP', required=True,
                        accessor=MAAttrAccessor('destination')
                        ),
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    MADateAndTimeDescription(
                        name='happened', label='Happened', required=True, accessor=MAAttrAccessor('happened')
                        ),
                    ]
                )
            # !TODO Change to reference initialization via constructor when it is available
            desc_container[0].reference = GlossaryDescriptor.description_for("Protocol")
            desc_container[1].reference = cls.description_for("IP4")

        elif fact_type == "CleartextCredentials":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    # !TODO Change to MAPasswordDescription when it is available
                    MAStringDescription(
                        name='password', label='Password', required=True, accessor=MAAttrAccessor('password')
                        ),
                    MAStringDescription(name='realm', label='Realm', accessor=MAAttrAccessor('realm')),
                    ]
                )

        elif fact_type == "NTLMv1Response":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    # !TODO Change to MABlobDescription (or MAPasswordDescription?) when it is available
                    MAStringDescription(
                        name='response', label='Response', required=True, accessor=MAAttrAccessor('response')
                        ),
                    MAStringDescription(name='realm', label='Realm', accessor=MAAttrAccessor('realm')),
                    ]
                )

        elif fact_type == "NTLMv2Response":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    # !TODO Change to MABlobDescription (or MAPasswordDescription?) when it is available
                    MAStringDescription(
                        name='response', label='Response', required=True, accessor=MAAttrAccessor('response')
                        ),
                    MAStringDescription(name='realm', label='Realm', accessor=MAAttrAccessor('realm')),
                    ]
                )

        elif fact_type == "NTHash":
            desc_container.setChildren(
                [
                    MAStringDescription(
                        name='username', label='Username', required=True, accessor=MAAttrAccessor('username')
                        ),
                    # !TODO Change to MABlobDescription (or MAPasswordDescription?) when it is available
                    MAStringDescription(
                        name='nt_hash', label='NT Hash', required=True, accessor=MAAttrAccessor('hash')
                        ),
                    MAStringDescription(name='realm', label='Realm', accessor=MAAttrAccessor('realm')),
                    ]
                )

        else:
            raise ValueError(f"Unknown fact type: {fact_type}.")

        return desc_container
        
# ==================== End of Domain-specific helper classes (for demo). ====================
'''


if __name__ == "__main__":

    # ==================== Scalar values testing. ====================
    print(" ==================== Scalar values testing. ====================")
    int_value = 123
    int_desc = MAIntDescription(name='TestInt', label='Test Int', default=0, accessor=MAIdentityAccessor())
    int_encoder = MAValueJsonWriter(int_desc)
    print(f"jsonable value for int_value: {int_encoder.write_json(int_value)}.")
    print(f"json string for int_value: {int_encoder.write_json_string(int_value)}.")

    str_value = 'abc'
    str_desc = MAStringDescription(name='TestString', label='Test String', default='', accessor=MAIdentityAccessor())
    str_encoder = MAValueJsonWriter(str_desc)
    print(f"jsonable value for str_value: {str_encoder.write_json(str_value)}.")
    print(f"json string for str_value: {str_encoder.write_json_string(str_value)}.")

    float_value = 1.23
    float_desc = MAFloatDescription(name='TestFloat', label='Test Float', default=0.0, accessor=MAIdentityAccessor())
    float_encoder = MAValueJsonWriter(float_desc)
    print(f"jsonable value for float_value: {float_encoder.write_json(float_value)}.")
    print(f"json string for float_value: {float_encoder.write_json_string(float_value)}.")

    date_value = datetime.now()
    date_desc = MADateAndTimeDescription(
        name='TestDate', label='Test Date', default=datetime.now(), accessor=MAIdentityAccessor()
        )
    date_encoder = MAValueJsonWriter(date_desc)
    print(f"jsonable value for date_value: {date_encoder.write_json(date_value)}.")
    print(f"json string for date_value: {date_encoder.write_json_string(date_value)}.")

    scalar_rel_value = int_value
    scalar_rel_desc = MARelationDescription(
        name='TestScalarRel', label='Test Scalar Relation', accessor=MAIdentityAccessor()
        )
    # Cannot set reference in constructor because of current MARelationDescription implementation.
    scalar_rel_desc.reference = int_desc
    scalar_rel_encoder = MAValueJsonWriter(scalar_rel_desc)
    print(f"jsonable value for scalar_rel_value: {scalar_rel_encoder.write_json(scalar_rel_value)}.")
    print(f"json string for scalar_rel_value: {scalar_rel_encoder.write_json_string(scalar_rel_value)}.")

    # ==================== Object encoding testing. ====================
    print(" ==================== Object encoding testing. ====================")
    object1 = TestObject1('object1', 123, 1.23, datetime.now())
    object_desc = MAContainer()
    object_desc.setChildren(
        [
            MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
            MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
            MAFloatDescription(
                name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
                ),
            MADateAndTimeDescription(
                name='date_value', label='Date Value', default=datetime.now(), accessor=MAAttrAccessor('date_value'),
                ),
            ]
        )
    object_encoder = MAObjectJsonWriter(object_desc)
    print(f"jsonable value for object1: {object_encoder.write_json(object1)}.")
    print(f"json string for object1: {object_encoder.write_json_string(object1)}.")

    # ==================== Object reference value testing. ====================
    print(" ==================== Object reference value testing. ====================")
    object_rel_desc = MARelationDescription(
        name='TestObjectRel', label='Test Object Relation', accessor=MAIdentityAccessor()
        )
    # Cannot set reference in constructor because of current MARelationDescription implementation.
    object_rel_desc.reference = object_desc
    object_rel_encoder = MAValueJsonWriter(object_rel_desc)
    print(f"jsonable value for reference->object1: {object_rel_encoder.write_json(object1)}.")
    print(f"json string for reference->object1: {object_rel_encoder.write_json_string(object1)}.")

    # ==================== Compound object with reference testing. ====================
    print(" ==================== Compound object with reference testing. ====================")
    compound_object = TestObject2('object2', 234, 2.34, datetime.now(), object1)
    compound_object_desc = MAContainer()
    compound_object_desc.setChildren([
        MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
        MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
        MAFloatDescription(
            name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
            ),
        MADateAndTimeDescription(
            name='date_value', label='Date Value', default=datetime.now(), accessor=MAAttrAccessor('date_value'),
            ),
        MARelationDescription(name='ref_object', label='Referenced Object', accessor=MAAttrAccessor('ref_object')),
        ])
    # Cannot set reference in constructor because of current MARelationDescription implementation.
    compound_object_desc.children[4].reference = object_desc
    compound_object_encoder = MAObjectJsonWriter(compound_object_desc)
    print(f"jsonable value for compound_object: {compound_object_encoder.write_json(compound_object)}.")
    print(f"json string for compound_object: {compound_object_encoder.write_json_string(compound_object)}.")

    '''
    # Domain specific classes are not available in this module. Following code is left just for demo purposes.
    # MA<x>JsonWriter tests should be rewritten with test models from this package. 

    # ==================== Domain-specific models testing. ====================
    print(" ==================== Domain-specific models testing. ====================")
    service = Service(name='Test Service', standard_port=1234)
    service_encoder = MAObjectJsonWriter(GlossaryDescriptor.description_for('Service'))
    print(f"json dict: {service_encoder.write_json(service)}.")
    print(f"json string: {service_encoder.write_json_string(service)}.")

    action_type1 = ActionType(name='Test Action Type 1', needed_proxy_action=None)
    action_type2 = ActionType(name='Test Action Type 2', needed_proxy_action=action_type1)
    action_type_encoder = MAObjectJsonWriter(GlossaryDescriptor.description_for('ActionType'))
    print(f"json dict for action_type1: {action_type_encoder.write_json(action_type1)}.")
    print(f"json string for action_type1: {action_type_encoder.write_json_string(action_type1)}.")
    print(f"json dict for action_type2: {action_type_encoder.write_json(action_type2)}.")
    print(f"json string for action_type2: {action_type_encoder.write_json_string(action_type2)}.")

    protocol = Protocol(name='Test Protocol')
    protocol_encoder = MAObjectJsonWriter(GlossaryDescriptor.description_for('Protocol'))
    print(f"json dict for protocol: {protocol_encoder.write_json(protocol)}.")
    print(f"json string for protocol: {protocol_encoder.write_json_string(protocol)}.")

    facttype = FactType(name='Test Fact Type', needed_protocol=protocol)
    facttype_encoder = MAObjectJsonWriter(GlossaryDescriptor.description_for('FactType'))
    print(f"json dict for facttype: {facttype_encoder.write_json(facttype)}.")
    print(f"json string for facttype: {facttype_encoder.write_json_string(facttype)}.")

    ip4 = IP4(address='192.168.10.13')
    ip4_encoder = MAObjectJsonWriter(FactDescriptor.description_for('IP4'))
    print(f"json dict for ip4: {ip4_encoder.write_json(ip4)}.")
    print(f"json string for ip4: {ip4_encoder.write_json_string(ip4)}.")

    port = Port(ip4_addr=ip4, port_num=1234)
    port_encoder = MAObjectJsonWriter(FactDescriptor.description_for('Port'))
    print(f"json dict for port: {port_encoder.write_json(port)}.")
    print(f"json string for port: {port_encoder.write_json_string(port)}.")

    ip4_scope = IP4Scope(address='192.168.10.0', mask=24)
    ip4_scope_encoder = MAObjectJsonWriter(FactDescriptor.description_for('IP4Scope'))
    print(f"json dict for ip4_scope: {ip4_scope_encoder.write_json(ip4_scope)}.")
    print(f"json string for ip4_scope: {ip4_scope_encoder.write_json_string(ip4_scope)}.")

    me = Me(interface='eth0', ip4_addr=ip4, net=ip4_scope, gateway=ip4)
    me_encoder = MAObjectJsonWriter(FactDescriptor.description_for('Me'))
    print(f"json dict for me: {me_encoder.write_json(me)}.")
    print(f"json string for me: {me_encoder.write_json_string(me)}.")

    poisoning = Poisoning(protocol=protocol, source=ip4, searched_name='abc1234', happened=datetime.now())
    poisoning_encoder = MAObjectJsonWriter(FactDescriptor.description_for('Poisoning'))
    print(f"json dict for poisoning: {poisoning_encoder.write_json(poisoning)}.")
    print(f"json string for poisoning: {poisoning_encoder.write_json_string(poisoning)}.")

    incoming_session = IncomingSession(
        protocol=protocol, source=ip4, username='user1', happened=datetime.now(), caused_by=1
        )
    incoming_session_encoder = MAObjectJsonWriter(FactDescriptor.description_for('IncomingSession'))
    print(f"json dict for incoming_session: {incoming_session_encoder.write_json(incoming_session)}.")
    print(f"json string for incoming_session: {incoming_session_encoder.write_json_string(incoming_session)}.")

    relayed_session = RelayedSession(
        protocol=protocol, destination=ip4, username='user1', happened=datetime.now()
        )
    relayed_session_encoder = MAObjectJsonWriter(FactDescriptor.description_for('RelayedSession'))
    print(f"json dict for relayed_session: {relayed_session_encoder.write_json(relayed_session)}.")
    print(f"json string for relayed_session: {relayed_session_encoder.write_json_string(relayed_session)}.")

    cleartext_credentials = CleartextCredentials(username='user1', password='P@ssw0rd', realm='acme.local')
    cleartext_credentials_encoder = MAObjectJsonWriter(FactDescriptor.description_for('CleartextCredentials'))
    print(f"json dict for cleartext_credentials: {cleartext_credentials_encoder.write_json(cleartext_credentials)}.")
    print(
        f"json string for cleartext_credentials: "
        f"{cleartext_credentials_encoder.write_json_string(cleartext_credentials)}."
        )

    ntlmv1response = NTLMv1Response(username='user1', response='0b0a9c9d9f0e0', realm='acme.local')
    ntlmv1response_encoder = MAObjectJsonWriter(FactDescriptor.description_for('NTLMv1Response'))
    print(f"json dict for ntlmv1response: {ntlmv1response_encoder.write_json(ntlmv1response)}.")
    print(f"json string for ntlmv1response: {ntlmv1response_encoder.write_json_string(ntlmv1response)}.")

    ntlmv2response = NTLMv2Response(username='user1', response='0b0a9c9d9f0e0', realm='acme.local')
    ntlmv2response_encoder = MAObjectJsonWriter(FactDescriptor.description_for('NTLMv2Response'))
    print(f"json dict for ntlmv2response: {ntlmv2response_encoder.write_json(ntlmv2response)}.")
    print(f"json string for ntlmv2response: {ntlmv2response_encoder.write_json_string(ntlmv2response)}.")

    nthash = NTHash(username='user1', nt_hash='0b0a9c9d9f0e0', realm='acme.local')
    nthash_encoder = MAObjectJsonWriter(FactDescriptor.description_for('NTHash'))
    print(f"json dict for nthash: {nthash_encoder.write_json(nthash)}.")
    print(f"json string for nthash: {nthash_encoder.write_json_string(nthash)}.")
    '''
