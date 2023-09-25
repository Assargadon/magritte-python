from unittest import TestCase
from MATimeDescription_class import MATimeDescription
from datetime import datetime
import MAMagnitudeDescriptionTest


class TestProperties_of_MATimeDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MATimeDescription()


class MATimeDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MATimeDescription()
        self.assertEqual(desc.kind, datetime)