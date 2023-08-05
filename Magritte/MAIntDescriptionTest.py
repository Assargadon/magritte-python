from unittest import TestCase
from MAIntDescription_class import MAIntDescription
import MANumberDescriptionTest

class TestProperties_of_MAIntDescription(MANumberDescriptionTest.TestProperties_of_MANumberDescription):

    def get_description_instance_to_test(self):
        return MAIntDescription()

class MAIntDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAIntDescription()

    def test_kind_by_default(self):
        self.assertEqual(self.desc.kind, int)

