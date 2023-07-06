from unittest import TestCase
from Magritte.MAAttrAccessor_class import MAAttrAccessor


class Person:

    def __init__(self, aName, aSurname, aAge, aGender):
        self.name = aName
        self.surname = aSurname
        self._age = None
        self.setAge(aAge)
        self.gender = aGender

    def information(self):
        print(f'{self.name} {self.surname} {self.age} {self.gender}')

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, aAge):
        self._age = aAge

