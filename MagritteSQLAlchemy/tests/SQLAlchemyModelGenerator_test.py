from unittest import TestCase

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from MagritteSQLAlchemy.SQLAlchemyModelGenerator import SQLAlchemyModelGenerator

# Please set the connection string before run this test. Make sure to create the sqlalchemy_test database if not exists
conn_str = "postgresql://postgres:secret@magritte-python-postgres/sqlalchemy_test"


class SQLAlchemyModelGeneratorTest(TestCase):

    def setUp(self):
        self.org_desc = TestModelDescriptor.description_for("Organization")
        self.user_desc = TestModelDescriptor.description_for("User")
        self.acc_desc = TestModelDescriptor.description_for("Account")
        self.host_desc = TestModelDescriptor.description_for("Host")
        self.port_desc = TestModelDescriptor.description_for("Port")
        self.modelGen = SQLAlchemyModelGenerator()
        self.modelGen.create_engine(conn_str)

    def test_canCreateModels(self):
        try:
            self.org_model = self.modelGen.generate_model(self.org_desc)
            self.user_model = self.modelGen.generate_model(self.user_desc)
            self.acc_model = self.modelGen.generate_model(self.acc_desc)
            self.host_model = self.modelGen.generate_model(self.host_desc)
            self.port_model = self.modelGen.generate_model(self.port_desc)

            self.modelGen.create_models()
        except:
            self.fail("The exception was raised in the SQL Alchemy models create process")

    def tearDown(self):
        self.modelGen.drop_models()
