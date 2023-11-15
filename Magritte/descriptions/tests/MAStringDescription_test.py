from unittest import TestCase
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.tests.MAElementDescription_test import TestProperties_of_MAElementDescription


class TestProperties_of_MAStringDescription(TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MAStringDescription()


class MAStringDescriptionTest(TestCase):

    def setUp(self):
        self.inst = MAStringDescription()

    def test_default_kind(self):
        self.assertEqual(self.inst.kind, str)

    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)