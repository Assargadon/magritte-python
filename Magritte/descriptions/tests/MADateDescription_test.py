from unittest import TestCase
from datetime import date

from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.tests.MAMagnitudeDescription_test import TestProperties_of_MAMagnitudeDescription


class TestProperties_of_MADateDescription(TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MADateDescription()


class MADateDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MADateDescription()
        self.assertEqual(desc.kind, date)