from unittest import TestCase
from Magritte.MAVariableAccessor_class import MAVariableAccessor


class Person:

    def __init__(self, aName, aSurname, aAge, aGender):
        self.name = aName
        self.surname = aSurname
        self.age = aAge
        self.gender = aGender

    def information(self):
        print(self.name + " " + self.surname + " " + self.age + " " + self.gender)



class MAVariableAccessorTest(TestCase):

    def test_canRead_plus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("name")

        self.assertEqual(inst.canRead(aModel), True)

    def test_canRead_minus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("canWrite")

        self.assertEqual(inst.canRead(aModel), False)

    def test_canWrite_plus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("surname")

        self.assertEqual(inst.canWrite(aModel), True)

    def test_canWrite_minus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("canWrite")

        self.assertEqual(inst.canWrite(aModel), False)

    def test_read_plus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("name")

        self.assertEqual(inst.read(aModel), "Aleks")

    def test_read_minus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("canWrite")

        self.assertEqual(inst.read(aModel), None)

    def test_write_plus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("name")

        inst.write(aModel, "Sam")

        self.assertEqual(inst.read(aModel), "Sam")

    def test_write_minus(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MAVariableAccessor("canWrite")

        inst.write(aModel, "Sam")

        self.assertEqual(inst.read(aModel), None)

    def test_getName(self):
        inst = MAVariableAccessor("name")

        self.assertEqual(inst.name, "name")

    def test_setName(self):
        inst = MAVariableAccessor("name")
        inst.name = "12345"

        self.assertEqual(inst.name, "12345")

    def test_isAbstract(self):
        self.assertEqual(MAVariableAccessor.isAbstract(), False)