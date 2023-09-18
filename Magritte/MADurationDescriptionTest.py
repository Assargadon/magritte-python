from unittest import TestCase
from MADurationDescription_class import MADurationDescription
from datetime import timedelta
import MAMagnitudeDescriptionTest


class TestProperties_of_MADurationDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADurationDescription()


class MADurationDescriptionTest(TestCase):
    def test_default_kind(self):
        desc = MADurationDescription()
        self.assertEqual(desc.kind, timedelta)
