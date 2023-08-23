from unittest import TestCase
from MADateAndTimeDescription_class import MADateAndTimeDescription
from datetime import datetime
import MAMagnitudeDescriptionTest


class TestProperties_of_MADateAndTimeDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADateAndTimeDescription()


class MADateAndTimeDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADateAndTimeDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, datetime)
