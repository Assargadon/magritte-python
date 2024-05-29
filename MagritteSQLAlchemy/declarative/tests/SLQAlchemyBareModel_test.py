from unittest import TestCase

from sqlalchemy import create_engine, Column, Integer, Identity, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Session

# Please set the connection string before run this test. Make sure to create the sqlalchemy_test database if not exists
conn_str = "postgresql://postgres:secret@magritte-python-postgres/sqlalchemy_test"


class Base(DeclarativeBase):
    pass


class Port(Base):
    __tablename__ = "port_sql"
    id = mapped_column(Integer, Identity(start=1, cycle=True), primary_key=True)
    numofports = mapped_column(Integer)
    host_id = Column(Integer, ForeignKey('host_sql.id'))
    host = relationship("Host", back_populates="ports")


class Host(Base):
    __tablename__ = "host_sql"
    id = mapped_column(Integer, Identity(start=1, cycle=True), primary_key=True)
    ip = mapped_column("ip", String)
    ports = relationship("Port", back_populates="host")


class SQLAlchemyModelGeneratorTest(TestCase):
    _engine = None

    def setUp(self):
        self.create_engine(conn_str)

    def test_canCreateModels(self):
        try:
            self.create_models()
            self.create_test_data(self._engine)
        except:
            self.fail("The exception was raised in the SQL Alchemy models create process")

    def tearDown(self):
        self.drop_models()

    def create_engine(self, conn_str):
        if self._engine is None:
            self._engine = create_engine(conn_str, echo=True)

    def create_models(self):
        Base.metadata.create_all(self._engine)

    def drop_models(self):
        Base.metadata.drop_all(self._engine)

    def create_test_data(self, engine):
        with Session(engine) as session:
            port_25_local = Port(numofports="25")
            port_80_local = Port(numofports="80")

            port_80_ext = Port(numofports="80")
            port_443_ext = Port(numofports="443")

            host_local = Host(ip='192.168.1.1', ports=[port_25_local, port_80_local])
            host_ext = Host(ip='8.8.8.8', ports=[port_80_ext, port_443_ext], )

            session.add_all([host_local, host_ext])

            session.commit()
