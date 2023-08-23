from unittest import TestCase
from MAFloatDescription_class import MAFloatDescription
import MAMagnitudeDescriptionTest


class TestProperties_of_MAFloatDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MAFloatDescription()


class MAFloatDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAFloatDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, float)
