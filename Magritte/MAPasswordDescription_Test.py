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
        self.assertFalse(self.inst1.isObfuscated(''))
        self.assertFalse(self.inst1.isObfuscated(None))
        self.assertFalse(self.inst1.isObfuscated(123))
        self.assertFalse(self.inst1.isObfuscated('**1'))
        self.assertTrue(self.inst1.isObfuscated('********'))

    def test_obfuscated(self):
        self.assertEqual(self.inst1.obfuscated(None), '')
        self.assertEqual(self.inst1.obfuscated('Hello'), '*****')
        self.assertEqual(self.inst1.obfuscated('foobar'), '******')
