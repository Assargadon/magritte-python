from unittest import TestCase
from datetime import datetime

from descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from descriptions.tests.MAMagnitudeDescriptionTest import TestProperties_of_MAMagnitudeDescription


class TestProperties_of_MADateAndTimeDescription(TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADateAndTimeDescription()


class MADateAndTimeDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MADateAndTimeDescription()
        self.assertEqual(desc.kind, datetime)
