from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from unittest import TestCase

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests import (Organization, Host, User, Port, Account, SubscriptionPlan, SoftwarePackage, )
from MagritteSQLAlchemy.experiments import registrator

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription

model_names = ('Organization', 'Host', 'Port', 'User', 'Account', 'SubscriptionPlan', 'SoftwarePackage')
descriptions = {k: v for k, v in ((x, TestModelDescriptor.description_for(x)) for x in model_names)}

env_description = MAContainer()
env_description.name = 'Environment'
env_description.label = 'Environment'
env_description.setChildren(
    [
        MAToOneRelationDescription(
            name='organization',
            label='Organization',
            required=True,
            accessor=MAAttrAccessor('organization'),
            classes=[Organization],
            reference=descriptions['Organization'],
            ),
        MAToManyRelationDescription(
            name='hosts',
            label='Hosts',
            required=True,
            accessor=MAAttrAccessor('hosts'),
            classes=[Host],
            reference=descriptions['Host'],
            ),
        MAToManyRelationDescription(
            name='ports',
            label='Ports',
            required=True,
            accessor=MAAttrAccessor('ports'),
            classes=[Port],
            reference=descriptions['Port'],
            ),
        MAToManyRelationDescription(
            name='users',
            label='Users',
            required=True,
            accessor=MAAttrAccessor('users'),
            classes=[User],
            reference=descriptions['User'],
            ),
        MAToManyRelationDescription(
            name='accounts',
            label='Accounts',
            required=True,
            accessor=MAAttrAccessor('accounts'),
            classes=[Account],
            reference=descriptions['Account'],
            ),
        ]
    )

registry = registrator.register(*descriptions.values())


class TestRegistratorExample(TestCase):
    def setUp(self):

        self.engine = create_engine("sqlite://", echo=True)
        # conn_str = "postgresql://postgres:postgres@localhost/sqlalchemy"
        # engine = create_engine(conn_str, echo=True)

        registry.metadata.create_all(self.engine)

        self.env = TestEnvironmentProvider()

    def tearDown(self):
        registry.metadata.drop_all(self.engine)

    def test_insert_then_count(self):
        with Session(self.engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *(sp for host in self.env.hosts for sp in host.software)
                ])
            session.commit()

        with Session(self.engine) as session:
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
            # sp_count = session.query(SubscriptionPlan).count()
            # self.assertEqual(sp_count, len(list(user.plan for user in self.env.users))) # Missing mapping for SingleOption?
            # software_count = session.query(SoftwarePackage).count() # Missing back_populates option?
            # self.assertEqual(software_count, sum(len(host.software) for host in self.env.hosts))

    def test_insert_then_query(self):
        with Session(self.engine) as session:
            session.add_all([
                self.env.organization,
                *self.env.hosts,
                *self.env.ports,
                *self.env.users,
                *self.env.accounts,
                *(sp for host in self.env.hosts for sp in host.software)
                ])
            session.commit()

        with Session(self.engine) as session:
            # For the test reasons let's find all the ports with port number < 150
            ports = session.query(Port).filter(Port._numofport < 150).all()
            self.assertTrue(all(port.numofport < 150 for port in ports))
            hosts = session.query(Host).filter(Host.ip is not None).all()
            self.assertTrue(all(host.ip for host in hosts))
            accounts = session.query(Account).filter(Account.login is not None).all()
            self.assertTrue(all(account.login for account in accounts))
            users = session.query(User).filter(User.regnum is not None).all()
            self.assertTrue(all(user.regnum for user in users))
            organizations = session.query(Organization).all()
            self.assertTrue(all(organization.name for organization in organizations))
            subscription_plans = session.query(SubscriptionPlan).filter(SubscriptionPlan.name is not None).all() # Filtering doesn't work?
            self.assertTrue(all(subscription_plan.name for subscription_plan in subscription_plans))
            # software_packages = session.query(SoftwarePackage).all()
            # self.assertTrue(all(software_package.name for software_package in software_packages))
