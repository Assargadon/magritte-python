from MAPasswordDescription_class import MAPasswordDescription
import MAStringDescriptionTest
from unittest import TestCase


class TestProperties_of_MAPasswordDescription(MAStringDescriptionTest.TestProperties_of_MAStringDescription):
    def get_description_instance_to_test(self):
        return MAPasswordDescription()

class MAPasswordDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAPasswordDescription()

    def test_isObfuscated(self):
        self.assertTrue(self.inst1.isObfuscated('********'))

    def test_obfuscated(self):
        self.assertEqual(self.inst1.obfuscated('Hello'), '*****')
