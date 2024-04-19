import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import unittest
from unittest import TestCase

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
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
descriptions = {k: v for k, v in ((x, TestModelDescriptor.description_for(x)) for x in model_names)}

registry = registrator.register(*descriptions.values())
engine = create_engine("sqlite://", echo=False)
# conn_str = "postgresql://postgres:postgres@localhost/registrator_test"
# engine = create_engine(conn_str, echo=True)

class TestRegistratorExample(TestCase):

    def setUp(self):

        registry.metadata.create_all(engine)
        self.env = TestEnvironmentProvider()

        self.org_name = self.env.organization.name
        self.host_ips = [host.ip for host in self.env.hosts]
        self.port_nums = [port.numofport for port in self.env.ports]
        self.user_regnums = [user.regnum for user in self.env.users]
        self.account_logins = [account.login for account in self.env.accounts]
        self.software_names = [software.name for software in self.env.software]

    def tearDown(self):
        registry.metadata.drop_all(engine)
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
                # *self.env.subscription_plans,
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
            # subscr_plans_count = session.query(SubscriptionPlan).count()
            # self.assertEqual(subscr_plans_count, len(self.env.subscription_plans))

    def test_insert_then_query(self):
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


if __name__ == '__main__':

    unittest.main()
