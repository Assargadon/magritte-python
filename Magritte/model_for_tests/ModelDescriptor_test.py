import datetime
import itertools

from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MADescriptionProvider import MADescriptionProvider
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.model_for_tests.Organization import Organization
from Magritte.model_for_tests.Account import Account
from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
from Magritte.model_for_tests.User import User
from Magritte.model_for_tests.SubscriptionPlan import SubscriptionPlan
from Magritte.model_for_tests.SoftwarePackage import SoftwarePackage


class TestModelDescriptorProvider(MADescriptionProvider):

    def instatiate_descriptions(self):
        subscription_plan_desc_container = MAContainer()
        user_desc_container = MAContainer()
        org_desc_container = MAContainer()
        acc_desc_container = MAContainer()
        host_desc_container = MAContainer()
        port_desc_container = MAContainer()
        soft_desc_container = MAContainer()

        soft_desc_container.kind = SoftwarePackage
        soft_desc_container.name = 'SoftwarePackage'
        soft_desc_container.label = 'Software Package model'
        soft_desc_container.setChildren(
            [
                MAStringDescription(
                    name='name', label='Name', required=True, accessor=MAAttrAccessor('name')
                ),
                MAStringDescription(
                    name='version', label='Version', required=True, accessor=MAAttrAccessor('version')
                ),
            ]
        )

        subscription_plan_desc_container.kind = SubscriptionPlan
        subscription_plan_desc_container.name = 'SubscriptionPlan'
        subscription_plan_desc_container.label = 'Subscription Plan model'
        subscription_plan_desc_container.setChildren(
            [
                MAStringDescription(
                    name='name', label='Name', required=True, accessor=MAAttrAccessor('name'),
                    sa_isPrimaryKey=True,
                ),
                MAIntDescription(
                    name='price', label='Price (per month)', required=True, accessor=MAAttrAccessor('price'),

                ),
                MAStringDescription(
                    name='description', label='Description of the plan features', required=False,
                    accessor=MAAttrAccessor('description'),
                ),
            ]
        )

        user_desc_container.kind = User
        user_desc_container.name = 'User'
        user_desc_container.label = 'User model'
        user_desc_container.setChildren(
            [
                MAStringDescription(
                    name='regnum', label='RegNum', required=True, accessor=MAAttrAccessor('regnum'),
                    sa_isPrimaryKey=True, sa_attrName='_regnum',
                ),
                MAStringDescription(
                    name='fio', label='FIO', required=True, accessor=MAAttrAccessor('fio'), sa_attrName='_fio',
                ),
                MADateDescription(
                    name='dateofbirth', label='DateOfBirth',
                    required=True, accessor=MAAttrAccessor('dateofbirth'),
                    sa_attrName='_dateofbirth',
                ),
                MAStringDescription(
                    name='gender', label='Gender', required=True, accessor=MAAttrAccessor('gender'),
                    sa_attrName='_gender',
                ),
                MAToOneRelationDescription(
                    name='organization', label='Organization', required=True,
                    accessor=MAAttrAccessor('organization'), classes=[Organization],
                    reference=org_desc_container,
                ),
                MADateDescription(
                    name='dateofadmission', label='DateOfAdmission',
                    required=True, accessor=MAAttrAccessor('dateofadmission'), sa_attrName='_dateofadmission',
                ),
                MADateDescription(
                    name='dateofdeparture', label='DateOfDeparture',
                    required=False, accessor=MAAttrAccessor('dateofdeparture'), sa_attrName='_dateofdeparture',
                ),
                MAToManyRelationDescription(
                    name='setofaccounts', label='SetOfAccounts', required=True,
                    accessor=MAAttrAccessor('setofaccounts'), classes=[Account],
                    reference=acc_desc_container,
                ),
                MASingleOptionDescription(
                    name='plan', label='Subscription Plan', required=False, accessor=MAAttrAccessor('plan'),
                    options=SubscriptionPlan.entries(),
                    reference=subscription_plan_desc_container
                ),
                # MAToOneRelationDescription(
                #    name='plan', label='Subscription Plan', required=False,
                #    accessor=MAAttrAccessor('plan'), classes=[SubscriptionPlan],
                #    reference=subscription_plan_desc_container,
                #    ),
            ]
        )

        org_desc_container.kind = Organization
        org_desc_container.name = 'Organization'
        org_desc_container.label = 'Organization model'
        org_desc_container.setChildren(
            [
                MAStringDescription(
                    name='name', label='Name', required=True, accessor=MAAttrAccessor('name'),
                    sa_isPrimaryKey=True, sa_attrName='_name',
                ),
                MAStringDescription(
                    name='address', label='Address', required=True, accessor=MAAttrAccessor('address'),
                    sa_attrName='_address',
                ),
                MABooleanDescription(
                    name='active', label='Active', required=True, accessor=MAAttrAccessor('active'),
                    sa_attrName='_active',
                ),
                MAToManyRelationDescription(
                    name='listusers', label='List of Users', required=True,
                    accessor=MAAttrAccessor('listusers'), classes=[User],
                    reference=user_desc_container,
                ),
                MAToManyRelationDescription(
                    name='listcomp', label='List of Computers', required=True,
                    accessor=MAAttrAccessor('listcomp'), classes=[Host],
                    reference=host_desc_container,
                ),
            ]
        )

        acc_desc_container.kind = Account
        acc_desc_container.name = 'Account'
        acc_desc_container.label = 'Account model'
        acc_desc_container.setChildren(
            [
                MAStringDescription(
                    name='login', label='Login', required=True, accessor=MAAttrAccessor('login'),
                    sa_isPrimaryKey=True, sa_attrName='_login',
                ),
                # !TODO Change to MAPasswordDescription when it is implemented
                MAStringDescription(
                    name='password', label='Password', required=True, accessor=MAAttrAccessor('password'),
                    sa_attrName='_password',
                ),
                # !TODO Change to MAPasswordDescription when it is implemented
                MAStringDescription(
                    name='ntlm', label='NTLM', accessor=MAAttrAccessor('ntlm'),
                    sa_attrName='_ntlm',
                ),
                MADateAndTimeDescription(
                    name='reg_timestamp', label='Timestamp Of Registration',
                    required=True, accessor=MAAttrAccessor('reg_timestamp'),
                    sa_attrName='_reg_timestamp',
                ),
                MAIntDescription(
                    name='days', label='Days valid', required=True, accessor=MAAttrAccessor('days'),
                    sa_attrName='_time',
                    ),
                MAToOneRelationDescription(
                    name='port', label='Port', required=True,
                    accessor=MAAttrAccessor('port'), classes=[Port],
                    reference=port_desc_container,
                ),
            ]
        )

        host_desc_container.kind = Host
        host_desc_container.name = 'Host'
        host_desc_container.label = 'Host model'
        host_desc_container.setChildren(
            [
                MAStringDescription(
                    name='ip', label='IP Address', required=True, accessor=MAAttrAccessor('ip'),
                    sa_isPrimaryKey=True, sa_attrName='_ip',
                ),
                MAToManyRelationDescription(
                    name='ports', label='Ports', required=True,
                    accessor=MAAttrAccessor('ports'), classes=[Port],
                    reference=port_desc_container,
                    sa_attrName='_ports',
                ),
                MAToManyRelationDescription(
                    name='software', label='Software', required=True,
                    accessor=MAAttrAccessor('software'), classes=[SoftwarePackage],
                    reference=soft_desc_container,
                    sa_attrName='_software',
                ),
            ]
        )

        port_desc_container.kind = Port
        port_desc_container.name = 'Port'
        port_desc_container.label = 'Port model'
        port_desc_container.setChildren(
            [
                MAIntDescription(
                    name='numofport', label='Number of Port', required=True, accessor=MAAttrAccessor('numofport'),
                    sa_attrName='_numofport', sa_isPrimaryKey=True,
                    ),
                MAToOneRelationDescription(
                    name='host', label='Host', required=True,
                    accessor=MAAttrAccessor('host'), classes=[Host], reference=host_desc_container,
                    sa_attrName='_host', sa_isPrimaryKey=True,
                    ),
                MASingleOptionDescription(
                    name='status', label='Status', required=False, accessor=MAAttrAccessor('status'),
                    options=Port.STATUSES,
                    reference=MAStringDescription(),
                    sa_attrName='_status'
                ),
                MAStringDescription(
                    accessor=MAAttrAccessor('label'), readOnly=True
                ),
            ]
        )

        self.register_description(subscription_plan_desc_container)
        self.register_description(subscription_plan_desc_container)
        self.register_description(user_desc_container)
        self.register_description(org_desc_container)
        self.register_description(acc_desc_container)
        self.register_description(host_desc_container)
        self.register_description(port_desc_container)
        self.register_description(soft_desc_container)



if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider

    descriptors = TestModelDescriptorProvider()

    org_desc = descriptors.description_for("Organization")
    user_desc = descriptors.description_for("User")
    acc_desc = descriptors.description_for("Account")
    host_desc = descriptors.description_for("Host")
    port_desc = descriptors.description_for("Port")
    soft_desc = descriptors.description_for("SoftwarePackage")

    test_env_provider = TestEnvironmentProvider()
    org = test_env_provider.organization
    users = test_env_provider.users
    accounts = test_env_provider.accounts
    hosts = test_env_provider.hosts
    ports = test_env_provider.ports
    soft = list(itertools.chain(*[host.software for host in hosts]))
    '''
    org = Organization.random_organization()
    users = org.listusers
    accounts = [account for user in users for account in user.setofaccounts]
    hosts = org.listcomp
    ports = [port for host in hosts for port in host.ports]
    '''

    print("Validating organization...")
    errs = org_desc.validate(org)
    for err in errs:
        print(f"Validation failed with {err}: {err.description.name}, {err.message}")
    print("Validation complete.")
    print(f"Organization: {org}")

    print("Validating users...")
    for user in users:
        errs = user_desc.validate(user)
        for err in errs:
            print(f"Validation failed with {err}: {err.description.name}, {err.message}")
            '''
            if err.description.name == 'dateofbirth':
                user_dob_desc = user_desc.detect(lambda x: x.name == 'dateofbirth')
                print(
                    f"type(user.dateofbirth) = {type(user.dateofbirth)}, "
                    f"user_dob_desc = {user_dob_desc}, "
                    f"user_desc['dateofbirth'].kind = {user_dob_desc.kind}"
                    )
            if err.description.name == 'setofaccounts':
                user_soa_desc = user_desc.detect(lambda x: x.name == 'setofaccounts')
                print(
                    f"type(user.setofaccounts) = {type(user.setofaccounts)}, "
                    f"user_desc['setofaccounts'].kind = {user_soa_desc.kind}"
                    )
            '''
    print("Validation complete.")
    print(f"Users: {users}")

    '''
    ! Cannot validate accounts because of the following issue:
    ! User.setofaccounts returns list(str) instead of list(Account)
    print("Validating accounts...")
    for account in accounts:
        errs = acc_desc.validate(account)
        for err in errs:
            if isinstance(err, AttributeError):
                print(f"Validation failed with {err}")
            else:
                print(f"Validation failed with {err}: {err.description}, {err.message}")
    print("Validation complete.")
    '''
    print("Validating hosts...")
    for host in hosts:
        errs = host_desc.validate(host)
        for err in errs:
            print(f"Validation failed with {err}: {err.description.name}, {err.message}")
    print("Validation complete.")
    print(f"Hosts: {hosts}")

    print("Validating ports...")
    for port in ports:
        errs = port_desc.validate(port)
        for err in errs:
            print(f"Validation failed with {err}: {err.description.name}, {err.message}")
    print("Validation complete.")
    print(f"Ports: {ports}")

    print("Validating software packages...")
    for sp in soft:
        errs = soft_desc.validate(sp)
        for err in errs:
            print(f"Validation failed with {err}: {err.description.name}, {err.message}")
    print("Validation complete.")
    print(f"Software packages: {soft}")

