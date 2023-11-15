from __init__ import append_paths

append_paths()

from unittest import TestCase

from datetime import date

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import Engine

from Magritte.MAContainer_class import MAContainer
from Magritte.MABooleanDescription_class import MABooleanDescription
from Magritte.MAStringDescription_class import MAStringDescription
from Magritte.MAIntDescription_class import MAIntDescription
from Magritte.MADateDescription_class import MADateDescription

from lib.MagritteSQL.db_deployer import DbDeployer

class DbDeployerTest(TestCase):

    def setUp(self) -> None:
        # Describing the Person table with a Magritte description
        self.persondesc = MAContainer(name='person', label = 'Person')
        self.persondesc += MAStringDescription(name='first_name', required=True)
        self.persondesc += MAStringDescription(name='last_name', required=True)
        self.persondesc += MABooleanDescription(name='is_active', required=False, default=True)
        self.persondesc += MADateDescription(name='dob', required=False)
        self.persondesc += MAIntDescription(name='height', required=False)
        self.persondesc += MAIntDescription(name='credit_score', required=False, default=5, min = 0, max = 10)
        # Describing an empty the Dummy table
        self.dummydesc = MAContainer(name='dummy', label = 'Dummy')

    def test_deploy_table_unregistered_model(self):
        deployer = DbDeployer.create_db_deployer("sqlite://")
        self.assertRaises(KeyError, deployer.deploy_table, "dummy")
        self.assertRaises(KeyError, deployer.get_registered_model, "dummy")

    def test_deploy_table_alreadyregistered_model(self):
        deployer = DbDeployer.create_db_deployer("sqlite://")
        deployer.register_model(self.dummydesc)
        self.assertRaises(InvalidRequestError, deployer.register_model, self.dummydesc)

    def test_deploy_table_registered_model(self):
        engine = create_engine("sqlite://")
        deployer = DbDeployer(engine)
        deployer.register_model(self.persondesc)
        deployer.deploy_table("person")

        personModel = deployer.get_registered_model("person")

        self.__test_required_first_name_constraint(engine, personModel)
        self.__test_required_last_name_constraint(engine, personModel)
        self.__test_min_max_credit_score_constraint(engine, personModel)
        self.__test_valid_person(engine, personModel)

    def __test_required_first_name_constraint(self, engine: Engine, personModel):
        with Session(engine) as session:
            sandy = personModel()
            session.add_all([sandy])
            self.assertRaises(IntegrityError, session.commit)

    def __test_required_last_name_constraint(self, engine: Engine, personModel):
        # Adding the data
        with Session(engine) as session:
            sandy = personModel(
                first_name="Sandy"
            )
            session.add_all([sandy])
            self.assertRaises(IntegrityError, session.commit)

    def __test_min_max_credit_score_constraint(self, engine: Engine, personModel):
        # Adding the data
        with Session(engine) as session:
            sandy = personModel(
                first_name="Sandy",
                last_name="Cheeks",
                credit_score=11,
            )
            session.add_all([sandy])
            self.assertRaises(IntegrityError, session.commit)

    def __test_valid_person(self, engine: Engine, personModel):
        person_first_name = "Spongebob"
        person_last_name = "Squarepants"
        person_dob = date(2022, 10, 22)
        person_height = 179
        # Adding the data
        with Session(engine) as session:
            spongebob = personModel(
                first_name=person_first_name,
                last_name=person_last_name,
                dob=person_dob,
                height=person_height,
            )
            session.add_all([spongebob])
            session.commit()
        # Fetching the data from a database
        with Session(engine) as session:
            stmt = select(personModel)
            result = list(session.scalars(stmt))
            self.assertEqual(1, len(result))
            self.assertEqual(person_first_name, result[0].first_name)
            self.assertEqual(person_last_name, result[0].last_name)
            self.assertEqual(person_dob, result[0].dob)
            self.assertEqual(person_height, result[0].height)
