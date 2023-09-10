from unittest import TestCase
from MANumberDescription_class import MANumberDescription
import MAMagnitudeDescriptionTest

class TestProperties_of_MANumberDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MANumberDescription()

class MANumberDescriptionTest(TestCase):

    def test_bePositive(self):
        desc = MANumberDescription()
        desc.bePositive()
        
        self.assertEqual(len(desc._validateConditions(5)), 0, "5 is positive, no errors expected")
        self.assertEqual(len(desc._validateConditions(-5)), 1, "-5 is negative, error should be found")
        self.assertEqual(len(desc._validateConditions(0)), 1, "zero is NOT positive, so error should be found")
