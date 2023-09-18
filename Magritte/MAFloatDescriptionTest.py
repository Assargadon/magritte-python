from unittest import TestCase
from MAFloatDescription_class import MAFloatDescription
import MAMagnitudeDescriptionTest


class TestProperties_of_MAFloatDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MAFloatDescription()


class MAFloatDescriptionTest(TestCase):
    def test_default_kind(self):
        desc = MAFloatDescription()
        self.assertEqual(desc.kind, float)
