from unittest import TestCase

from sqlalchemy import create_engine

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from MagritteSQLAlchemy.SQLAlchemyModelGenerator import SQLAlchemyModelGenerator

# Please set the connection string before run this test. Make sure to create the sqlalchemy_test database if not exists
conn_str = "postgresql://postgres:secret@magritte-python-postgres/sqlalchemy_test"


class SQLAlchemyModelGeneratorTest(TestCase):
    _engine = None

    def setUp(self):
        self.org_desc = TestModelDescriptor.description_for("Organization")
        self.user_desc = TestModelDescriptor.description_for("User")
        self.acc_desc = TestModelDescriptor.description_for("Account")
        self.host_desc = TestModelDescriptor.description_for("Host")
        self.port_desc = TestModelDescriptor.description_for("Port")
        self.modelGen = SQLAlchemyModelGenerator()
        self.create_engine(conn_str)

    def test_canCreateModels(self):
        try:
            self.org_model = self.modelGen.generate_model(self.org_desc)
            self.user_model = self.modelGen.generate_model(self.user_desc)
            self.acc_model = self.modelGen.generate_model(self.acc_desc)
            self.host_model = self.modelGen.generate_model(self.host_desc)
            self.port_model = self.modelGen.generate_model(self.port_desc)

            self.create_models()
        except:
            self.fail("The exception was raised in the SQL Alchemy models create process")

    def tearDown(self):
        self.drop_models()

    def create_engine(self, conn_str):
        if self._engine is None:
            self._engine = create_engine(conn_str, echo=True)

    def create_models(self):
        self.modelGen.base_class.metadata.create_all(self._engine)

    def drop_models(self):
        self.modelGen.base_class.metadata.drop_all(self._engine)
