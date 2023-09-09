from unittest import TestCase
from MAToManyRelationDescription_class import MAToManyRelationDescription
import MARelationDescriptionTest


class TestProperties_of_MAToManyRelationDescription(MARelationDescriptionTest.TestProperties_of_MARelationDescription):
    def get_description_instance_to_test(self):
        return MAToManyRelationDescription()



class MAToManyRelationDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToManyRelationDescription()

    # nothing special to test, reserved for the future
