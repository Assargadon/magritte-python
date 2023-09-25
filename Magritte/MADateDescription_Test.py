from unittest import TestCase
from MADateDescription_class import MADateDescription
from datetime import datetime
import MAMagnitudeDescriptionTest


class TestProperties_of_MADateDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADateDescription()


class MADateDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MADateDescription()
        self.assertEqual(desc.kind, datetime)