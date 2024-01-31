import datetime

from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.model_for_tests.Organization import Organization
from Magritte.model_for_tests.Account import Account
from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
from Magritte.model_for_tests.User import User


class TestModelDescriptor:
    @classmethod
    def description_for(cls, model_type: str) -> MAContainer:
        """Returns a fact description for the given fact type."""

        user_desc_container = MAContainer()
        org_desc_container = MAContainer()
        acc_desc_container = MAContainer()
        host_desc_container = MAContainer()
        port_desc_container = MAContainer()

        user_desc_container.kind = User
        user_desc_container.name = 'User'
        user_desc_container.label = 'User model'
        user_desc_container.setChildren(
            [
                MAStringDescription(
                    name='regnum', label='RegNum', required=True, accessor=MAAttrAccessor('regnum')
                    ),
                MAStringDescription(
                    name='fio', label='FIO', required=True, accessor=MAAttrAccessor('fio')
                    ),
                MADateDescription(
                    name='dateofbirth', label='DateOfBirth',
                    required=True, accessor=MAAttrAccessor('dateofbirth'),
                    ),
                MAStringDescription(
                    name='gender', label='Gender', required=True, accessor=MAAttrAccessor('gender')
                    ),
                MAToOneRelationDescription(
                    name='organization', label='Organization', required=True,
                    accessor=MAAttrAccessor('organization'), classes=[Organization],
                    reference=org_desc_container,
                    ),
                MADateDescription(
                    name='dateofadmission', label='DateOfAdmission',
                    required=True, accessor=MAAttrAccessor('dateofadmission'),
                    ),
                MADateDescription(
                    name='dateofdeparture', label='DateOfDeparture',
                    required=True, accessor=MAAttrAccessor('dateofdeparture'),
                    ),
                MAToManyRelationDescription(
                    name='setofaccounts', label='SetOfAccounts', required=True,
                    accessor=MAAttrAccessor('setofaccounts'), classes=[Account],
                    reference=acc_desc_container,
                    ),
                ]
            )

        org_desc_container.kind = Organization
        org_desc_container.name = 'Organization'
        org_desc_container.label = 'Organization model'
        org_desc_container.setChildren(
            [
                MAStringDescription(
                    name='name', label='Name', required=True, accessor=MAAttrAccessor('name')
                    ),
                MAStringDescription(
                    name='address', label='Address', required=True, accessor=MAAttrAccessor('address')
                    ),
                MABooleanDescription(
                    name='active', label='Active', required=True, accessor=MAAttrAccessor('active')
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
                    name='login', label='Login', required=True, accessor=MAAttrAccessor('login')
                    ),
                #!TODO Change to MAPasswordDescription when it is implemented
                MAStringDescription(
                    name='password', label='Password', required=True, accessor=MAAttrAccessor('password')
                    ),
                # !TODO Change to MAPasswordDescription when it is implemented
                MAStringDescription(
                    name='ntlm', label='NTLM', accessor=MAAttrAccessor('ntlm')
                    ),
                MADateAndTimeDescription(
                    name='dateofreg', label='Date Of Registration',
                    required=True, accessor=MAAttrAccessor('dateofreg')
                    ),
                MAIntDescription(
                    name='days', label='Days valid', required=True, accessor=MAAttrAccessor('days')
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
                    name='ip', label='IP Address', required=True, accessor=MAAttrAccessor('ip')
                    ),
                MAToManyRelationDescription(
                    name='ports', label='Ports', required=True,
                    accessor=MAAttrAccessor('ports'), classes=[Port],
                    reference=port_desc_container,
                    ),
                ]
            )

        port_desc_container.kind = Port
        port_desc_container.name = 'Port'
        port_desc_container.label = 'Port model'
        port_desc_container.setChildren(
            [
                MAIntDescription(
                    name='numofport', label='Number of Port', required=True, accessor=MAAttrAccessor('numofport')
                    ),
                MAToOneRelationDescription(
                    name='host', label='Host', required=True,
                    accessor=MAAttrAccessor('host'), classes=[Host],
                    reference=host_desc_container,
                    ),
                ]
            )

        if model_type == 'User':
            return user_desc_container
        elif model_type == 'Organization':
            return org_desc_container
        elif model_type == 'Account':
            return acc_desc_container
        elif model_type == 'Host':
            return host_desc_container
        elif  model_type == 'Port':
            return port_desc_container
        else:
            raise ValueError(f"Unknown model type: {model_type}")


if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider

    org_desc = TestModelDescriptor.description_for("Organization")
    user_desc = TestModelDescriptor.description_for("User")
    acc_desc = TestModelDescriptor.description_for("Account")
    host_desc = TestModelDescriptor.description_for("Host")
    port_desc = TestModelDescriptor.description_for("Port")

    test_env_provider = TestEnvironmentProvider()
    org = test_env_provider.organization
    users = test_env_provider.users
    accounts = test_env_provider.accounts
    hosts = test_env_provider.hosts
    ports = test_env_provider.ports
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
