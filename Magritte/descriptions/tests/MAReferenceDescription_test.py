from unittest import TestCase

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.tests.MAElementDescription_test import TestProperties_of_MAElementDescription


class TestProperties_of_MAReferenceDescription(TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MAReferenceDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('reference', MADescription, True)
        }

class MAReferenceDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAReferenceDescription()

    def test_copy(self):
        copy_test = self.inst1.__copy__()
        self.assertEqual(copy_test, self.inst1)

    def test_reference(self):
        self.assertIsInstance(self.inst1.reference, MADescription)
        self.inst1.reference = MAStringDescription(name = "First Name")
