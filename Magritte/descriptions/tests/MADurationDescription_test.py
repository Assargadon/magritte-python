from unittest import TestCase
from datetime import timedelta

from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.tests.MAMagnitudeDescription_test import TestProperties_of_MAMagnitudeDescription


class TestProperties_of_MADurationDescription(TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADurationDescription()


class MADurationDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MADurationDescription()
        self.assertEqual(desc.kind, timedelta)
