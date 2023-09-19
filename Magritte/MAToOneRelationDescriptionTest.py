from unittest import TestCase
from MAToOneRelationDescription_class import MAToOneRelationDescription
import MARelationDescriptionTest


class TestProperties_of_MAToOneRelationDescription(MARelationDescriptionTest.TestProperties_of_MARelationDescription):
    def get_description_instance_to_test(self):
        return MAToOneRelationDescription()



class MAToOneRelationDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToOneRelationDescription()

    # nothing special to test, reserved for the future
