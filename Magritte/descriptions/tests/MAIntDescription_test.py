from unittest import TestCase

from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.tests.MANumberDescription_test import TestProperties_of_MANumberDescription

class TestProperties_of_MAIntDescription(TestProperties_of_MANumberDescription):

    def get_description_instance_to_test(self):
        return MAIntDescription()

class MAIntDescriptionTest(TestCase):

    def test_default_kind(self):
        desc = MAIntDescription()
        self.assertEqual(desc.kind, int)

