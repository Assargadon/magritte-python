from unittest import TestCase
from MAFloatDescription_class import MAFloatDescription
import MAMagnitudeDescriptionTest


class TestProperties_of_MAFloatDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MAFloatDescription()


class MAFloatDescriptionTest(TestCase):

    def test_beInteger(self):
        desc = MAFloatDescription()
        desc.beInteger()
        
        self.assertEqual(len(desc._validateConditions(5.1)), 1, "5.1 is not integer, error should be found")
        self.assertEqual(len(desc._validateConditions(5.0)), 0, "5.0 is integer, no errors expected")


    def test_default_kind(self):
        desc = MAFloatDescription()
        self.assertEqual(desc.kind, float)
