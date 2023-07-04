from unittest import TestCase
from Magritte.MASelectorAccessor_class import MASelectorAccessor


class Person:

    def __init__(self, aName, aSurname, aAge, aGender):
        self.name = aName
        self.surname = aSurname
        self.age = aAge
        self.gender = aGender

    def information(self):
        print(self.name + " " + self.surname + " " + str(self.age) + " " + self.gender)

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age


class MASelectorAccessorTest(TestCase):

    def test_canRead_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "set_age")

        self.assertEqual(inst.canRead(aModel), True)

    def test_canRead_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("read", "set_age")

        self.assertEqual(inst.canRead(aModel), False)

    def test_canWrite_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "set_age")

        self.assertEqual(inst.canWrite(aModel), True)

    def test_canWrite_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "write")

        self.assertEqual(inst.canWrite(aModel), False)

    def test_read_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "set_age")

        self.assertEqual(inst.read(aModel), 23)

    def test_read_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("read", "set_age")

        with self.assertRaises(Exception):
            inst.read(aModel)

    def test_write_positive(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "set_age")

        inst.write(aModel, 25)

        self.assertEqual(aModel.get_age(), 25)

    def test_write_negative(self):
        aModel = Person("Aleks", "Hofman", 23, "man")
        inst = MASelectorAccessor("get_age", "write")

        with self.assertRaises(Exception):
            inst.write(aModel, 25)

    def test_getReadSelector(self):
        inst = MASelectorAccessor("get_age", "set_age")

        self.assertEqual(inst.readSelector, "get_age")

    def test_setReadSelector(self):
        inst = MASelectorAccessor("get_age", "set_age")
        inst.readSelector = "read"

        self.assertEqual(inst.readSelector, "read")

    def test_getWriteSelector(self):
        inst = MASelectorAccessor("get_age", "set_age")

        self.assertEqual(inst.writeSelector, "set_age")

    def test_setWriteSelector(self):
        inst = MASelectorAccessor("get_age", "set_age")
        inst.writeSelector = "write"

        self.assertEqual(inst.writeSelector, "write")

    def test_isAbstract(self):
        self.assertEqual(MASelectorAccessor.isAbstract(), False)
