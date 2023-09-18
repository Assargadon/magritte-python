from unittest import TestCase
from MAIntDescription_class import MAIntDescription
import MANumberDescriptionTest

class TestProperties_of_MAIntDescription(MANumberDescriptionTest.TestProperties_of_MANumberDescription):

    def get_description_instance_to_test(self):
        return MAIntDescription()

class MAIntDescriptionTest(TestCase):
    def test_default_kind(self):
        desc = MAIntDescription()
        self.assertEqual(desc.kind, int)

