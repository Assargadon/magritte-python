from unittest import TestCase
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from datetime import time
import Magritte.descriptions.tests.MAMagnitudeDescription_test as MAMagnitudeDescription_test


class TestProperties_of_MATimeDescription(MAMagnitudeDescription_test.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MATimeDescription()


class MATimeDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MATimeDescription()
        self.assertEqual(desc.kind, time)