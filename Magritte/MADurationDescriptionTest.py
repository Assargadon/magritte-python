from unittest import TestCase
from MADurationDescription_class import MADurationDescription
from datetime import timedelta
import MAMagnitudeDescriptionTest


class TestProperties_of_MADurationDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADurationDescription()


class MADurationDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADurationDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, timedelta)
