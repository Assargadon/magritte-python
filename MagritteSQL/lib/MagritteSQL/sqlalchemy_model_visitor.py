from datetime import date
from typing import Any, Optional

from Magritte.visitors.MAVisitor_class import MAVisitor

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase

# Compulsory class for SQLAlchemy needs
class Base(DeclarativeBase):
    pass

class SQLAlchemyModelVisitor(MAVisitor):

    # We're about to generate a model class to represent table with support of SQLAlchemy. Let's take following Person class as an example:

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
            False: Mapped[Optional[date]],
            True: Mapped[date],
        },
    }

    def convert(self, model, description = None):
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
        element = self.convert(model, description)
        self.model = prev_model
        return element

    def visitContainer(self, description):
        if not self.element:
            self.element = {}
            self.visitAll(description)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self.element")

    def visitElementDescription(self, description):
        value = description.accessor.read(self.model)
        if isinstance(value, (int, float, str, bool)) and description.name in {'label','name','type','required','default','min','max'}:
            self.element[description.name] = value

    def visitToManyRelationDescription(self, description):
        collection = description.accessor.read(self.model)
        if collection is None:
            self.sqlAlchemyTableType = None
        else:
            clsAnnotations = {'id': Mapped[int]}
            members = {'__tablename__': self.element['name'],
                       'id': mapped_column(primary_key=True)}
            for entry in collection:
                element = self.deeper(entry)
                clsAnnotations[element['name']] = self.magritteSqlAlchemyAnnotationTypes[element['type']][element['required']]
                members[element['name']] = self.get_mapped_column(element)
            members['__annotations__'] = clsAnnotations
            members['__repr__'] = lambda self: '{{{0}}}'.format(', '.join("%s: %s" % (name, getattr(self, name)) for name in clsAnnotations))
            self.sqlAlchemyTableType = type(self.element['label'],
                                            (Base,),
                                            members)

    def get_mapped_column(self, element):

        def get_check_constraint(name, min, max):
            return CheckConstraint('{0} >= {1} AND {0} <= {2}'.format(name, min, max))

        if 'default' in element and 'min' in element and 'max' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], get_check_constraint(element['name'], element['min'], element['max']), default=element['default'])
        elif 'default' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], default=element['default'])
        elif 'min' in element and 'max' in element:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']], get_check_constraint(element['name'], element['min'], element['max']))
        else:
            return mapped_column(self.magritteSqlAlchemyMappedTypes[element['type']])
