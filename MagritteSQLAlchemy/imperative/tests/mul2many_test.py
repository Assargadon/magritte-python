import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import unittest
from unittest import TestCase

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
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


class Host:
    def __init__(self):
        self.ip = None
        self.users = []
        self.admins = []

class User:
    def __init__(self):
        self.name = None

class Env:
    def __init__(self):
        self.hosts = []
        self.users = []

model_names = ('Host', 'User')

host_desc = MAContainer()
user_desc = MAContainer()

host_desc.name = "Host"
host_desc.kind = Host
host_desc.setChildren([
    MAStringDescription(name="ip", accessor=MAAttrAccessor("ip"), required=True),
    MAToManyRelationDescription(
        name="users",
        accessor=MAAttrAccessor("users"),
        classes=[User],
        reference=user_desc,
    ),
    MAToManyRelationDescription(
        name="admins",
        accessor=MAAttrAccessor("admins"),
        classes=[User],
        reference=user_desc,
        ),
])

user_desc.name = "User"
user_desc.kind = User
user_desc.setChildren([
    MAStringDescription(name="name", accessor=MAAttrAccessor("name"), required=True),
])

descriptions = {"Host": host_desc, "User": user_desc}

registry = registrator.register(*descriptions.values())
# engine = create_engine("sqlite://", echo=False)
conn_str = "postgresql://postgres:secret@localhost/registrator_m2m_test"
engine = create_engine(conn_str, echo=True)

class TestRegistratorExample(TestCase):

    def setUp(self):

        registry.metadata.create_all(engine)
        self.env = Env()
        self.env.hosts = [Host() for _ in range(3)]
        self.env.users = [User() for _ in range(3)]

        self.env.hosts[0].ip = "192.168.0.1"
        self.env.hosts[1].ip = "192.168.0.2"
        self.env.hosts[2].ip = "192.168.0.3"
        self.env.users[0].name = "user1"
        self.env.users[1].name = "user2"
        self.env.users[2].name = "user3"
        self.env.hosts[0].users = [self.env.users[0], self.env.users[1]]
        self.env.hosts[1].users = [self.env.users[1], self.env.users[2]]
        self.env.hosts[2].users = [self.env.users[0], self.env.users[2]]
        self.env.hosts[0].admins = [self.env.users[0]]

        self.host_ips = [host.ip for host in self.env.hosts]
        self.user_names = [user.name for user in self.env.users]


    def tearDown(self):
        registry.metadata.drop_all(engine)


    def test_insert_then_count(self):
        with Session(engine) as session:
            session.add_all([
                *self.env.hosts,
                *self.env.users,
                ])
            session.commit()

        with Session(engine) as session:
            # Verify count of each model
            host_count = session.query(Host).count()
            self.assertEqual(host_count, len(self.env.hosts))
            user_count = session.query(User).count()
            self.assertEqual(user_count, len(self.env.users))

    def test_insert_then_query(self):
        with Session(engine) as session:
            session.add_all([
                *self.env.hosts,
                *self.env.users,
                ])
            session.commit()

        with Session(engine) as session:
            # Query objects by a specific field value of the first model of its class
            hosts = session.query(Host).filter(Host.ip == self.host_ips[0]).first()
            self.assertEqual(hosts.ip, self.host_ips[0])
            users = session.query(User).filter(User.name == self.user_names[0]).first()
            self.assertEqual(users.name, self.user_names[0])

    def test_insert_remove1_then_query(self):
        with Session(engine) as session:
            session.add_all([
                *self.env.hosts,
                *self.env.users,
                ])
            session.commit()

        with Session(engine) as session:

            # Count objects before removal
            host_count_before = session.query(Host).count()
            user_count_before = session.query(User).count()

            session.query(User).filter(User.name == self.user_names[0]).delete()
            session.commit()
            user_count_after = session.query(User).count()
            expected_removed_count = self.user_names.count(self.user_names[0])
            self.assertEqual(user_count_after, user_count_before - expected_removed_count)

            session.query(Host).filter(Host.ip == self.host_ips[0]).delete()
            session.commit()
            host_count_after = session.query(Host).count()
            expected_removed_count = self.host_ips.count(self.host_ips[0])
            self.assertEqual(host_count_after, host_count_before - expected_removed_count)


if __name__ == '__main__':

    unittest.main()
