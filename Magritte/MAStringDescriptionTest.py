from unittest import TestCase
from Magritte.MAStringDescription_class import MAStringDescription
import MAElementDescriptionTest


class TestProperties_of_MAStringDescription(MAElementDescriptionTest.TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MAStringDescription()



class MAStringDescriptionTest(TestCase):

    def setUp(self):
        self.inst = MAStringDescription()

    def test_isAbstract(self):
        self.assertEqual(MAStringDescription.isAbstract(), False)

    def test_Kind(self):
        self.assertEqual(self.inst.kind, str)

    def test_Label(self):
        self.assertEqual(self.inst.label, 'str')

    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)