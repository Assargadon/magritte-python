from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from MagritteSQLAlchemy.experiments import registrator
import sqlalchemy

if __name__ == '__main__':
    descriptions = [TestModelDescriptor.description_for(x) for x in (
        'User', 'Organization', 'Account', 'Host', 'Port', 'SubscriptionPlan',
        )]

    registry = registrator.register(*descriptions)

    engine = create_engine("sqlite://", echo=True)
    registry.metadata.create_all(engine)

    env = TestEnvironmentProvider()

    with Session(engine) as session:
        session.add_all([
            env.organization,
            *env.hosts,
            *env.ports,
            *env.users,
            *env.accounts,
            ])
        session.commit()

