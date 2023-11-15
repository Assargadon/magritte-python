from unittest import TestCase

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor


class Person:

    def __init__(self, aName, aSurname, aAge, aGender):
        self._name = aName
        self.surname = aSurname
        self._age = None
        self.age = aAge
        self.gender = aGender
        self.noneAttr = None

    def information(self):
        print(f'{self.name} {self.surname} {self.age} {self.gender}')

    @property
    def age(self):
        return self._age

    @property
    def name(self):
        return self._name

    @age.setter
    def age(self, aAge):
        self._age = aAge


class MAAttrAccessorTest(TestCase):

    def setUp(self):
        self.aModel = Person("Aleks", "Hofman", 23, "man")
        self.accessor_field = MAAttrAccessor("surname")
        self.accessor_property = MAAttrAccessor("age")
        self.accessor_readOnly = MAAttrAccessor("name")
        self.accessor_missingAttr = MAAttrAccessor("read")
        self.accessor_noneAttr = MAAttrAccessor("noneAttr")

    def test_canRead(self):
        self.assertEqual(self.accessor_field.canRead(self.aModel), True)
        self.assertEqual(self.accessor_property.canRead(self.aModel), True)
        self.assertEqual(self.accessor_readOnly.canRead(self.aModel), True)
        self.assertEqual(self.accessor_missingAttr.canRead(self.aModel), False)
        self.assertEqual(self.accessor_noneAttr.canRead(self.aModel), True)

    def test_canWrite(self):
        self.assertEqual(self.accessor_field.canWrite(self.aModel), True)
        self.assertEqual(self.accessor_property.canWrite(self.aModel), True)
        self.assertEqual(self.accessor_readOnly.canWrite(self.aModel), False)
        self.assertEqual(self.accessor_missingAttr.canWrite(self.aModel), False)
        self.assertEqual(self.accessor_noneAttr.canWrite(self.aModel), True)

    def test_read(self):
        self.assertEqual(self.accessor_field.read(self.aModel), "Hofman")
        self.assertEqual(self.accessor_property.read(self.aModel), 23)
        self.assertEqual(self.accessor_readOnly.read(self.aModel), "Aleks")
        with self.assertRaises(Exception):
            self.accessor_missingAttr.read(self.aModel)

    def test_write_positive(self):
        self.accessor_field.write(self.aModel, "Butcher")
        self.accessor_property.write(self.aModel, 25)

        with self.assertRaises(Exception):
            self.accessor_readOnly.write(self.aModel, "Billy")

        self.accessor_missingAttr.write(self.aModel, 30)

        self.assertEqual(self.accessor_field.read(self.aModel), "Butcher")
        self.assertEqual(self.accessor_property.read(self.aModel), 25)
        self.assertEqual(self.accessor_missingAttr.read(self.aModel), 30)

    def test_name(self):

        self.assertEqual(self.accessor_field.name, "surname")


class TestPerson():
    def __init__(
            self, 
            first_name, 
            age, 
            height, 
            alive, 
            active, 
    ):
        self.first_name = first_name
        self.age = age
        self.height = height
        self.alive = alive
        self.active = active

class MABoolAttrAccessorTest(TestCase):

    def testSimplePrint(self):
        
        model = TestPerson(
            first_name="Bob", 
            age=33.8, 
            height=180, 
            alive=False,
            active=False
        )

        aliveAccessor = MAAttrAccessor('alive')
        activeAccessor = MAAttrAccessor('active')

#        print(f'alive: ${aliveAccessor.read(model)}')
#        print(f'active: ${activeAccessor.read(model)}')

        self.assertIsInstance(aliveAccessor.read(model), bool)
        self.assertIsInstance(activeAccessor.read(model), bool)
