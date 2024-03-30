from sqlalchemy import create_engine

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from MagritteSQLAlchemy.experiments import registrator
import sqlalchemy

if __name__ == '__main__':
    descriptions = [TestModelDescriptor.description_for(x) for x in (
        'User', 'Organization', 'Account', 'Host', 'Port', 'SubscriptionPlan',
        )]

    registry = registrator.register(*descriptions)

#    engine = create_engine("sqlite://", echo=True)
    conn_str = "postgresql://postgres:postgres@localhost/sqlalchemy"
    engine = create_engine(conn_str, echo=True)



    registry.metadata.create_all(engine)

    '''
    with Session(engine) as session:
        session.add_all([user])
        session.commit()
    '''
