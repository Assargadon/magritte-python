import logging
import os
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import unittest
from unittest import TestCase

from sqlalchemy.sql.ddl import CreateSchema

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests import (Organization, Host, User, Port, Account, SubscriptionPlan, SoftwarePackage, )
from MagritteSQLAlchemy.imperative import registrator

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    )

logger.setLevel(logging.DEBUG)
logging.getLogger("MagritteSQLAlchemy.imperative").setLevel(logging.DEBUG)
# Fine-grained logging
# logging.getLogger("MagritteSQLAlchemy.imperative.registrator").setLevel(logging.DEBUG)
# logging.getLogger("MagritteSQLAlchemy.imperative.fieldsmapper").setLevel(logging.DEBUG)
# logging.getLogger("MagritteSQLAlchemy.imperative.fkeysmapper").setLevel(logging.DEBUG)


model_names = ('Organization', 'Host', 'Port', 'User', 'Account', 'SubscriptionPlan', 'SoftwarePackage')
descriptors = TestModelDescriptorProvider()
descriptions = {k: v for k, v in ((x, descriptors.description_for(x)) for x in model_names)}

# engine = create_engine("sqlite://", echo=False)
conn_str = f"{os.getenv('CONN_STR_BASE', 'postgresql://postgres:secret@localhost')}/registrator_test"
engine = create_engine(conn_str, echo=True)


class NoPkModel:
    pass


def _make_model_class(name):
    return type(name, (), {})


def _make_descriptor(name, kind, children, should_generate_pk=True):
    descriptor = MAContainer(name=name)
    descriptor.kind = kind
    descriptor.sa_shouldGeneratePrimaryKey = should_generate_pk
    descriptor.setChildren(children)
    return descriptor


class TestRegistratorPrimaryKeyValidation(TestCase):

    def test_register_raises_when_no_primary_key_is_defined(self):
        descriptor = MAContainer()
        descriptor.kind = NoPkModel
        descriptor.name = "NoPkModel"
        descriptor.setChildren(
            [
                MAStringDescription(name="name", required=True),
            ]
        )

        with self.assertRaisesRegex(ValueError, "does not have primary keys"):
            registrator.register(descriptor)


class TestRegistratorPrimaryKeyGenerationRules(TestCase):

    def test_register_enables_db_generation_for_int_primary_key(self):
        kind = _make_model_class("GeneratedIntModel")
        descriptor = _make_descriptor(
            "GeneratedIntModel",
            kind,
            [
                MAIntDescription(
                    name="id",
                    required=True,
                    sa_isPrimaryKey=True,
                )
            ],
        )

        registry = registrator.register(descriptor)
        table = registry.metadata.tables["GeneratedIntModel"]

        self.assertIsNotNone(table.c.id.identity)

    def test_register_enables_db_generation_for_scalar_single_option_int_primary_key(self):
        kind = _make_model_class("GeneratedOptionModel")
        descriptor = _make_descriptor(
            "GeneratedOptionModel",
            kind,
            [
                MASingleOptionDescription(
                    name="status",
                    required=True,
                    sa_isPrimaryKey=True,
                    reference=MAIntDescription(name="status_code", required=True),
                )
            ],
        )

        registry = registrator.register(descriptor)
        table = registry.metadata.tables["GeneratedOptionModel"]

        self.assertIsNotNone(table.c.status.identity)

    def test_register_rejects_primary_keys_that_cannot_be_generated(self):
        cases = [
            (
                "string",
                MAStringDescription(name="name", required=True, sa_isPrimaryKey=True),
            ),
            (
                "boolean",
                MABooleanDescription(name="enabled", required=True, sa_isPrimaryKey=True),
            ),
        ]

        for case_name, pk_description in cases:
            with self.subTest(case_name=case_name):
                kind = _make_model_class(f"Generated{case_name.title()}PkModel")
                descriptor = _make_descriptor(
                    f"Generated{case_name.title()}PkModel",
                    kind,
                    [pk_description],
                )

                with self.assertRaisesRegex(ValueError, "cannot auto-generate primary key"):
                    registrator.register(descriptor)

    def test_register_logs_warning_when_multiple_primary_keys_are_marked(self):
        kind = _make_model_class("GeneratedCompositeModel")
        descriptor = _make_descriptor(
            "GeneratedCompositeModel",
            kind,
            [
                MAIntDescription(
                    name="left_id",
                    required=True,
                    sa_isPrimaryKey=True,
                ),
                MAIntDescription(
                    name="right_id",
                    required=True,
                    sa_isPrimaryKey=True,
                ),
            ],
        )

        with patch("MagritteSQLAlchemy.imperative.fieldsmapper.logger.warning") as warning_mock:
            registry = registrator.register(descriptor)

        table = registry.metadata.tables["GeneratedCompositeModel"]
        self.assertIsNotNone(table.c.left_id.identity)
        self.assertIsNotNone(table.c.right_id.identity)
        warning_mock.assert_called_once()


class TestRegistratorExample(TestCase):

    def setUp(self):
        try:
            delattr(SubscriptionPlan, '_entries')
        except AttributeError:
            pass
        self.registry = registrator.register(*descriptions.values())
        self.registry.metadata.create_all(engine)
        self.env = TestEnvironmentProvider()

        self.org_name = self.env.organization.name
        self.host_ips = [host.ip for host in self.env.hosts]
        self.port_nums = [port.numofport for port in self.env.ports]
        self.user_regnums = [user.regnum for user in self.env.users]
        self.account_logins = [account.login for account in self.env.accounts]
        self.software_names = [software.name for software in self.env.software]
        self.subscription_plan_names = [sp.name for sp in self.env.subscription_plans]

    def tearDown(self):
        self.registry.metadata.drop_all(engine)
        self.registry.dispose()
        delattr(SubscriptionPlan, '_entries')


    def test_insert_then_count(self):
        with Session(engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *self.env.software,
                *self.env.subscription_plans,
                ])
            session.commit()

        with Session(engine) as session:
            # Verify count of each model
            org_count = session.query(Organization).count()
            self.assertEqual(org_count, 1)
            host_count = session.query(Host).count()
            self.assertEqual(host_count, len(self.env.hosts))
            port_count = session.query(Port).count()
            self.assertEqual(port_count, len(self.env.ports))
            user_count = session.query(User).count()
            self.assertEqual(user_count, len(self.env.users))
            account_count = session.query(Account).count()
            self.assertEqual(account_count, len(self.env.accounts))
            software_count = session.query(SoftwarePackage).count()
            self.assertEqual(software_count, len(self.env.software))
            subscr_plans_count = session.query(SubscriptionPlan).count()
            self.assertEqual(subscr_plans_count, len(self.env.subscription_plans))

    def test_insert_then_query(self):
        with Session(engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *self.env.software,
                 *self.env.subscription_plans,
                ])
            session.commit()

        with Session(engine) as session:
            # Query objects by a specific field value of the first model of its class
            org = session.query(Organization).filter(Organization._name == self.org_name).first()
            self.assertEqual(org.name, self.org_name)
            hosts = session.query(Host).filter(Host._ip == self.host_ips[0]).first()
            self.assertEqual(hosts.ip, self.host_ips[0])
            ports = session.query(Port).filter(Port._numofport == self.port_nums[0]).first()
            self.assertEqual(ports.numofport, self.port_nums[0])
            users = session.query(User).filter(User._regnum == self.user_regnums[0]).first()
            self.assertEqual(users.regnum, self.user_regnums[0])
            accounts = session.query(Account).filter(Account._login == self.account_logins[0]).first()
            self.assertEqual(accounts.login, self.account_logins[0])
            software = session.query(SoftwarePackage).filter(SoftwarePackage.name == self.software_names[0]).first()
            self.assertEqual(software.name, self.software_names[0])
            subscription_plans = session.query(SubscriptionPlan).filter(SubscriptionPlan.name == self.subscription_plan_names[0]).first()
            self.assertEqual(subscription_plans.name, self.subscription_plan_names[0])

    '''
    # Removal is not yet supported by ORM: removal attempt leads to FK violation
    def test_insert_remove1_then_query(self):
        with Session(engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *self.env.software,
                # *self.env.subscription_plans,
                ])
            session.commit()

        with Session(engine) as session:

            # Count objects before removal
            org_count_before = session.query(Organization).count()
            host_count_before = session.query(Host).count()
            port_count_before = session.query(Port).count()
            user_count_before = session.query(User).count()
            account_count_before = session.query(Account).count()
            software_count_before = session.query(SoftwarePackage).count()
            # subscr_plans_count_before = session.query(SubscriptionPlan).count()

            # Remove objects by a specific field value of the first model of its class

            # session.query(SubscriptionPlan).filter(SubscriptionPlan.name == self.subscription_plan_names[0]).delete()
            # session.commit()
            # subscr_plans_count_after = session.query(SubscriptionPlan).count()
            # expected_removed_count = self.subscription_plan_names.count(self.subscription_plan_names[0])
            # self.assertEqual(subscr_plans_count_after, subscr_plans_count_before - expected_removed_count)

            session.query(Account).filter(Account._login == self.account_logins[0]).delete()
            session.commit()
            account_count_after = session.query(Account).count()
            expected_removed_count = self.account_logins.count(self.account_logins[0])
            self.assertEqual(account_count_after, account_count_before - expected_removed_count)

            session.query(User).filter(User._regnum == self.user_regnums[0]).delete()
            session.commit()
            user_count_after = session.query(User).count()
            expected_removed_count = self.user_regnums.count(self.user_regnums[0])
            self.assertEqual(user_count_after, user_count_before - expected_removed_count)

            session.query(SoftwarePackage).filter(SoftwarePackage.name == self.software_names[0]).delete()
            session.commit()
            software_count_after = session.query(SoftwarePackage).count()
            expected_removed_count = self.software_names.count(self.software_names[0])
            self.assertEqual(software_count_after, software_count_before - expected_removed_count)

            session.query(Port).filter(Port._numofport == self.port_nums[0]).delete()
            session.commit()
            port_count_after = session.query(Port).count()
            expected_removed_count = self.port_nums.count(self.port_nums[0])
            self.assertEqual(port_count_after, port_count_before - expected_removed_count)

            session.query(Host).filter(Host._ip == self.host_ips[0]).delete()
            session.commit()
            host_count_after = session.query(Host).count()
            expected_removed_count = self.host_ips.count(self.host_ips[0])
            self.assertEqual(host_count_after, host_count_before - expected_removed_count)

            session.query(Organization).filter(Organization._name == self.org_name).delete()
            session.commit()
            org_count_after = session.query(Organization).count()
            expected_removed_count = self.org_name.count(self.org_name)
            self.assertEqual(org_count_after, org_count_before - expected_removed_count)
    '''


class TestRegistratorExampleWithSchema(TestCase):

    def setUp(self):
        try:
            delattr(SubscriptionPlan, '_entries')
        except AttributeError:
            pass
        with engine.connect() as connection:
            connection.execute(CreateSchema("test_schema", if_not_exists=True))
            connection.commit()
        self.registry = registrator.register(*descriptions.values(), schema='test_schema')
        self.registry.metadata.create_all(engine)
        self.env = TestEnvironmentProvider()

        self.org_name = self.env.organization.name
        self.host_ips = [host.ip for host in self.env.hosts]
        self.port_nums = [port.numofport for port in self.env.ports]
        self.user_regnums = [user.regnum for user in self.env.users]
        self.account_logins = [account.login for account in self.env.accounts]
        self.software_names = [software.name for software in self.env.software]
        self.subscription_plan_names = [sp.name for sp in self.env.subscription_plans]

    def tearDown(self):
        self.registry.metadata.drop_all(engine)
        self.registry.dispose()
        delattr(SubscriptionPlan, '_entries')


    def test_insert_then_count(self):
        with Session(engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *self.env.software,
                *self.env.subscription_plans,
                ])
            session.commit()

        with Session(engine) as session:
            # Verify count of each model
            org_count = session.query(Organization).count()
            self.assertEqual(org_count, 1)
            host_count = session.query(Host).count()
            self.assertEqual(host_count, len(self.env.hosts))
            port_count = session.query(Port).count()
            self.assertEqual(port_count, len(self.env.ports))
            user_count = session.query(User).count()
            self.assertEqual(user_count, len(self.env.users))
            account_count = session.query(Account).count()
            self.assertEqual(account_count, len(self.env.accounts))
            software_count = session.query(SoftwarePackage).count()
            self.assertEqual(software_count, len(self.env.software))
            subscr_plans_count = session.query(SubscriptionPlan).count()
            self.assertEqual(subscr_plans_count, len(self.env.subscription_plans))

    def test_insert_then_query(self):
        with Session(engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *self.env.software,
                 *self.env.subscription_plans,
                ])
            session.commit()

        with Session(engine) as session:
            # Query objects by a specific field value of the first model of its class
            org = session.query(Organization).filter(Organization._name == self.org_name).first()
            self.assertEqual(org.name, self.org_name)
            hosts = session.query(Host).filter(Host._ip == self.host_ips[0]).first()
            self.assertEqual(hosts.ip, self.host_ips[0])
            ports = session.query(Port).filter(Port._numofport == self.port_nums[0]).first()
            self.assertEqual(ports.numofport, self.port_nums[0])
            users = session.query(User).filter(User._regnum == self.user_regnums[0]).first()
            self.assertEqual(users.regnum, self.user_regnums[0])
            accounts = session.query(Account).filter(Account._login == self.account_logins[0]).first()
            self.assertEqual(accounts.login, self.account_logins[0])
            software = session.query(SoftwarePackage).filter(SoftwarePackage.name == self.software_names[0]).first()
            self.assertEqual(software.name, self.software_names[0])
            subscription_plans = session.query(SubscriptionPlan).filter(SubscriptionPlan.name == self.subscription_plan_names[0]).first()
            self.assertEqual(subscription_plans.name, self.subscription_plan_names[0])


if __name__ == '__main__':

    unittest.main()
