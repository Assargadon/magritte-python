from unittest import TestCase
from Magritte.MAReferenceDescription_class import MAReferenceDescription
from Magritte.MAStringDescription_class import MAStringDescription


class MAReferenceDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAReferenceDescription()

    def test_copy(self):
        copy_test = self.inst1.__copy__()
        self.assertEqual(copy_test, self.inst1)

    def test_defaultReference(self):
        self.assertEqual(isinstance(MAReferenceDescription.defaultReference(), MAStringDescription), True)

    def test_getInitializer(self):
        self.assertEqual(self.inst1.initializer, self.inst1)

    def test_setInitializer(self):
        self.inst1.initializer = 123
        self.assertEqual(self.inst1.initializer, 123)

    def test_getReference(self):
        self.assertEqual(isinstance(self.inst1.reference, MAStringDescription), True)

    def test_setReference(self):
        self.inst1.reference = [1, 2, 3]
        self.assertEqual(self.inst1.reference, [1, 2, 3])
