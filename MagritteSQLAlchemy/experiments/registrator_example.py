from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
# from Magritte.model_for_tests import (Organization, Host, User, Port, Account, )
from MagritteSQLAlchemy.experiments import registrator
import sqlalchemy

if __name__ == '__main__':
    descriptions = [TestModelDescriptor.description_for(x) for x in (
        'Host', 'Port', #'User', 'Organization', 'Account', 'SubscriptionPlan',
        )]

    registry = registrator.register(*descriptions)

    # engine = create_engine("sqlite://", echo=True)
    conn_str = "postgresql://postgres:postgres@localhost/sqlalchemy"
    engine = create_engine(conn_str, echo=True)



    registry.metadata.create_all(engine)

    env = TestEnvironmentProvider()

    with Session(engine) as session:
        session.add_all([
            #env.organization,
            *env.hosts,
            *env.ports,
            #*env.users,
            #*env.accounts,
            ])
        session.commit()

    with Session(engine) as session:
        for desc in descriptions:
            count = session.query(desc.kind).count()
            print(f'count of {desc.name} = {count}')

