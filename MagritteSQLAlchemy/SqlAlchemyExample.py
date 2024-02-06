from pprint import pprint

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
from MagritteSQLAlchemy.SQLAlchemyModelGenerator import SQLAlchemyModelGenerator

# Please set the connection string before run this test. Make sure to create the sqlalchemy_test database if not exists
conn_str = "postgresql://postgres:secret@magritte-python-postgres/sqlalchemy_test"

provider = TestEnvironmentProvider()

port_desc = MAContainer()
port_desc.name = 'Port_Container'
host_desc = MAContainer()
host_desc.name = 'Host_Container'


port_desc += MAIntDescription(name='uid', accessor='uid', isPrimaryKey=True)
port_desc += MAStringDescription(name='numofport', accessor='numofport', label='Port number', required=True)
port_desc += MAToOneRelationDescription(name='host', accessor='host', label='Host', required=True, classes=[Host],
                                        reference=host_desc)

host_desc += MAIntDescription(name='uid', accessor='uid', isPrimaryKey=True)
host_desc += MAStringDescription(name='ip', accessor='ip', label='IP Address', required=True)
host_desc += MAToManyRelationDescription(name='ports', accessor='ports', label='Ports', required=True, classes=[Port],
                                         reference=port_desc)

# Let create model classed and create tables in the db if not existed
engine = create_engine(conn_str, echo=True)

modelGen = SQLAlchemyModelGenerator()
port_model = modelGen.generate_model(port_desc)
host_model = modelGen.generate_model(host_desc)
modelGen.base_class.metadata.create_all(engine)

# Let's save all hosts in to the database
db_hosts = []

print("Saving hosts to the db:")
for host in provider.hosts:
    db_host = host_model().copy_from(host)
    db_hosts.append(db_host)

# ... Now we use native SQL Alchemy calls to stores the data
with Session(engine) as session:
    session.add_all(db_hosts)
    session.commit()

# Lets loads all ports from the database
with Session(engine) as session:
    ports_selected = select(port_model)

for port in session.scalars(ports_selected):
    pprint(vars(port))
