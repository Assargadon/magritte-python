from unittest import TestCase
from Magritte.MAAttrAccessor_class import MAAttrAccessor


class Person:

    def __init__(self, aName, aSurname, aAge, aGender):
        self.name = aName
        self.surname = aSurname
        self._age = None
        self.age = aAge
        self.gender = aGender

    def information(self):
        print(f'{self.name} {self.surname} {self.age} {self.gender}')

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, aAge):
        self._age = aAge


class MAAttrAccessorTest(TestCase):

    def test_canRead_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("age")

        self.assertEqual(inst.canRead(aModel), True)

    def test_canRead_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("read")

        self.assertEqual(inst.canRead(aModel), False)

    def test_canWrite_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("age")

        self.assertEqual(inst.canWrite(aModel), True)

    def test_canWrite_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("write")

        self.assertEqual(inst.canWrite(aModel), False)

    def test_read_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("age")

        self.assertEqual(inst.read(aModel), 23)

    def test_read_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("read")

        with self.assertRaises(Exception):
            inst.read(aModel)

    def test_write_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("age")

        inst.write(aModel, 25)

        self.assertEqual(inst.read(aModel), 25)

    def test_write_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAAttrAccessor("write")

        with self.assertRaises(Exception):
            inst.write(aModel, 25)

    def test_isAbstract(self):
        self.assertEqual(MAAttrAccessor.isAbstract(), False)