from unittest import TestCase
from datetime import datetime
from typing import Any, Optional

from MAContainer_class import MAContainer
from MABooleanDescription_class import MABooleanDescription
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MADateDescription_class import MADateDescription
from MAVisitor_class import MAVisitor

from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

class TestSQLAlchemyVisitor(MAVisitor):

# We're about to generate following Person class to represent table with support of SQLAlchemy:

    # class Person(Base):
    #     __tablename__ = 'person'
    #     id: Mapped[int] = mapped_column(primary_key=True)
    #     first_name: Mapped[str] = mapped_column(String(50))
    #     last_name: Mapped[str] = mapped_column(String(50))
    #     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    #     dob: Mapped[Optional[datetime]] = mapped_column(Date)
    #     height: Mapped[Optional[int]] = mapped_column(Integer)
    #     credit_score: Mapped[int] = mapped_column(Integer, CheckConstraint('credit_score >= 0 AND credit_score <= 10'), default=5)

    #     def __repr__(self):
    #         return f"Person(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, is_active={self.is_active!r}, dob={self.dob!r}, height={self.height!r}, credit_score={self.credit_score!r})"

# We will rewrite this to create this class dynamically due to we're generating class from a Magritte description. It will look this:

    # cls_annotations = {'id': Mapped[int],
    #                    'first_name': Mapped[str],
    #                    'last_name': Mapped[str],
    #                    'is_active': Mapped[bool],
    #                    'dob':Mapped[Optional[datetime]],
    #                    'height':Mapped[Optional[int]],
    #                    'credit_score':Mapped[int]}
    # personType = type('Person',
    #                   (Base,),
    #                   {'__annotations__': cls_annotations,
    #                   '__tablename__': 'person',
    #                   'id': mapped_column(primary_key=True),
    #                   'first_name':mapped_column(String(50)),
    #                   'last_name':mapped_column(String(50)),
    #                   'is_active':mapped_column(Boolean, default=True),
    #                   'dob':mapped_column(Date),
    #                   'height':mapped_column(Integer),
    #                   'credit_score':mapped_column(Integer, CheckConstraint('credit_score >= 0 AND credit_score <= 10'), default=5),
    #                   '__repr__': lambda self: f"Person(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, is_active={self.is_active!r}, dob={self.dob!r}, height={self.height!r}, credit_score={self.credit_score!r})"})

    magritteSqlAlchemyMappedTypes: dict[str, Any] = {
        'MAIntDescription': Integer,
        'MAStringDescription': String(50),
        'MABooleanDescription': Boolean,
        'MADateDescription': Date,
    }

    magritteSqlAlchemyAnnotationTypes: dict[str, dict[bool, Any]] = {
        'MAIntDescription': {
            False: Mapped[Optional[int]],
            True: Mapped[int],
        },
        'MAStringDescription': {
            False: Mapped[Optional[str]],
            True: Mapped[str],
        },
        'MABooleanDescription': {
            False: Mapped[Optional[bool]],
            True: Mapped[bool],
        },
        'MADateDescription': {
            False: Mapped[Optional[datetime]],
            True: Mapped[datetime],
        },
    }

    def convert(self, model):
        self._convert(model)
        return self.sqlAlchemyTableType

    def _convert(self, model, description = None):
        if not description:
            try:
                description = model.magritteDescription()
            except (AttributeError, TypeError):
                print(f"?{model}?")
                return None
        self.element = None
        self.model = model
        self.visit(description)
        return self.element

    def deeper(self, model, description = None):
        if model is None: return None #to avoid same condition in every place needed to convert value 
        if isinstance(model, (int, float, str, bool)): return model
        prev_model = self.model
        element = self._convert(model, description)
        self.model = prev_model
        return element

    def visitContainer(self, description):
        if not self.element:
            self.element = {}
            self.visitAll(description)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self.element")

    def visitElementDescription(self, description):
        value = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        if isinstance(value, (int, float, str, bool)) and description.name in {'label','name','type','required','default','min','max'}:
            self.element[description.name] = value

    def visitToManyRelationDescription(self, description):
        collection = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        if collection is None:
            self.sqlAlchemyTableType = None
        else:
            clsAnnotations = {'id': Mapped[int]}
            members = {'__tablename__': self.element['name'],
                       'id': mapped_column(primary_key=True)}
            for entry in collection:
                element = self.deeper(entry)
                clsAnnotations[element['name']] = self.magritteSqlAlchemyAnnotationTypes[element['type']][element['required']]
                members[element['name']] = self.getMappedColumn(element)
            members['__annotations__'] = clsAnnotations
            members['__repr__'] = lambda self: '{{{0}}}'.format(', '.join("%s: %s" % (name, getattr(self, name)) for name in clsAnnotations))
            self.sqlAlchemyTableType = type(self.element['label'],
                                            (Base,),
                                            members)

    def getMappedColumn(self, element):

        def getCheckConstraint(name, min, max):
            return CheckConstraint('{0} >= {1} AND {0} <= {2}'.format(name, min, max))

        if 'default' in element and 'min' in element and 'max' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], getCheckConstraint(element['name'], element['min'], element['max']), default=element['default'])
        elif 'default' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], default=element['default'])
        elif 'min' in element and 'max' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], getCheckConstraint(element['name'], element['min'], element['max']))
        else:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']])

class PersonTest(TestCase):

    # Describing the Person table with a Magritte description
    personDesc = MAContainer(name='person', label = 'Person')
    personDesc += MAStringDescription(name='first_name', required=True)
    personDesc += MAStringDescription(name='last_name', required=True)
    personDesc += MABooleanDescription(name='is_active', required=False, default=True)
    personDesc += MADateDescription(name='dob', required=False)
    personDesc += MAIntDescription(name='height', required=False)
    personDesc += MAIntDescription(name='credit_score', required=False, default=5, min = 0, max = 10)

    objectEncoder = TestSQLAlchemyVisitor()

    personType = objectEncoder.convert(personDesc)

    # Embeeded SQLite DB. Suitable for the tests
    engine = create_engine("sqlite://", echo=False)
    # Creating the table
    personType.metadata.create_all(engine)   

    def test_checkRequiredFirstNameConstraint(self):
        # Adding the data
        with Session(self.engine) as session:
            try:
                sandy = self.personType(
                )
                session.add_all([sandy])
                session.commit()
            except Exception as e:
                print(e)
                return
            assert False

    def test_checkRequiredLastNameConstraint(self):
        # Adding the data
        with Session(self.engine) as session:
            try:
                sandy = self.personType(
                    first_name="Sandy"
                )
                session.add_all([sandy])
                session.commit()
            except Exception as e:
                print(e)
                return
            assert False

    def test_checkMinMaxCreditScoreConstraint(self):
        # Adding the data
        with Session(self.engine) as session:
            try:
                sandy = self.personType(
                    first_name="Sandy",
                    last_name="Cheeks",
                    credit_score=11,
                )
                session.add_all([sandy])
                session.commit()
            except Exception as e:
                print(e)
                return
            assert False

    def test_validPerson(self):
        # Adding the data
        with Session(self.engine) as session:
            spongebob = self.personType(
                first_name="Spongebob",
                last_name="Squarepants",
                dob=datetime(2022, 10, 22),
                height=179,
            )
            session.add_all([spongebob])
            session.commit()
        # Fetching the data from a database
        with Session(self.engine) as session:
            stmt = select(self.personType)
            print("Database content:")
            for person in session.scalars(stmt):
                print(person)
