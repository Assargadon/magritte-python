import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Magritte.MAModel_class import MAModel
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from MagritteSQLAlchemy.imperative import registrator

logger = logging.getLogger(__name__)


class Host(MAModel):
    address = ""
    protocol = ""


host_desc = MAContainer()
host_desc.name = 'Host'
host_desc.kind = Host
host_desc.setChildren(
    [
        MAStringDescription(
            name='address', label='Ip Address', required=True, accessor=MAAttrAccessor('address'),
            sa_isPrimaryKey=True,
            ),
        MAStringDescription(
            name='protocol', label='Protocol', required=True, accessor=MAAttrAccessor('protocol'),
            ),
        ]
    )


class Interface(MAModel):
    interface = ""
    ip4 = ""
    gateway = ""


interface_desc = MAContainer()
interface_desc.name = 'Interface'
interface_desc.kind = Interface
interface_desc.setChildren(
    [
        MAStringDescription(
            name='interface', label='Interface', required=True, accessor=MAAttrAccessor('interface')
            , sa_isPrimaryKey=True
            ),
        MAToOneRelationDescription(
            name='ip4_addr', label='IP4 Address', required=True,
            accessor=MAAttrAccessor('ip4_addr'), classes=[Host],
            reference=host_desc
            ),
        # MAToOneRelationDescription(
        #     name='gateway', label='Gateway', accessor=MAAttrAccessor('gateway'), classes=[Host],
        #     reference=host_desc
        #     )
        ]
    )

if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        )

    logger.setLevel(logging.DEBUG)
    logging.getLogger("MagritteSQLAlchemy.imperative").setLevel(logging.DEBUG)

    descriptions = [host_desc, interface_desc]

    registry = registrator.register(*descriptions)

    engine = create_engine("sqlite://", echo=True)
    # conn_str = "postgresql://postgres:postgres@localhost/sqlalchemy"
    # engine = create_engine(conn_str, echo=True)

    registry.metadata.create_all(engine)

    # Create some data
    hosts = [Host(address='192.168.0.1', protocol='http'), Host(address='192.168.0.2', protocol='https')]
    interfaces = [Interface(
        interface='eth0', ip4_addr=hosts[0],
        # gateway=hosts[1]
        )]

    with Session(engine) as session:
        session.add_all([*hosts, *interfaces])
        session.commit()

    with Session(engine) as session:
        for desc in descriptions:
            count = session.query(desc.kind).count()
            print(f'count of {desc.name} = {count}')

    # For the test reasons let's find all the ports with port number < 150
    with Session(engine) as session:
        interfaces = session.query(Interface).all()
        for interface in interfaces:
            print(
                f'interface = {interface.interface} IP4: {interface.ip4_addr.address} '
                # f'Gateway: {interface.gateway.address}'
                )
        hosts = session.query(Host).all()
        for host in hosts:
            print(f'host = {host.address} Protocol: {host.protocol}')
