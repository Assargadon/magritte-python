import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests import (Organization, Host, User, Port, Account, SubscriptionPlan, SoftwarePackage)
from MagritteSQLAlchemy import registrator

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        )

    logger.setLevel(logging.DEBUG)
    logging.getLogger("MagritteSQLAlchemy").setLevel(logging.DEBUG)
    # Fine-grained logging
    # logging.getLogger("MagritteSQLAlchemy.registrator").setLevel(logging.DEBUG)
    # logging.getLogger("MagritteSQLAlchemy.fieldsmapper").setLevel(logging.DEBUG)
    # logging.getLogger("MagritteSQLAlchemy.fkeysmapper").setLevel(logging.DEBUG)

    descriptions = [TestModelDescriptor.description_for(x) for x in (
        'User', 'Organization', 'Account', 'Host', 'Port', 'SubscriptionPlan', 'SoftwarePackage',
        )]

    registry = registrator.register(*descriptions)

    engine = create_engine("sqlite://", echo=False)
    # conn_str = "postgresql://postgres:postgres@localhost/sqlalchemy"
    # engine = create_engine(conn_str, echo=True)



    registry.metadata.create_all(engine)

    env = TestEnvironmentProvider()

    with Session(engine) as session:
        session.add_all([
            env.organization,
            *env.hosts,
            *env.ports,
            *env.users,
            *env.accounts,
            *env.subscription_plans,
            *(sp for host in env.hosts for sp in host.software)
            ])
        session.commit()

    with Session(engine) as session:
        for desc in descriptions:
            count = session.query(desc.kind).count()
            print(f'count of {desc.name} = {count}')


    # For the test reasons let's find all the ports with port number < 150
    with Session(engine) as session:
        ports = session.query(Port).filter(Port._numofport < 150).all()
        for port in ports:
            print(f'port = {port.label} - {port.status}')
        hosts = session.query(Host).all()
        for host in hosts:
            print(f'host = {host.ip} Software: {", ".join([str(item) for item in host.software])} ')
        accounts = session.query(Account).all()
        for account in accounts:
            print(f'account = {account.login} : {account.password}')
        users = session.query(User).all()
        for user in users:
            print(f'user = {user.regnum}: {user.fio} [{user.plan}]')
        organizations = session.query(Organization).all()
        for organization in organizations:
            print(f'organization = {organization.name} Hosts: {", ".join([str(item.ip) for item in organization.listcomp])}')
        subscription_plans = session.query(SubscriptionPlan).all()
        for subscription_plan in subscription_plans:
            print(f'subscription_plan = {subscription_plan.name} ')
        software_packages = session.query(SoftwarePackage).all()
        for software_package in software_packages:
            print(f'software_package = {software_package.name} ')
