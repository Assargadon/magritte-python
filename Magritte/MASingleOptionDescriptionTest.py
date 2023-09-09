from unittest import TestCase
from MASingleOptionDescription_class import MASingleOptionDescription
import MAOptionDescriptionTest


class TestProperties_of_MASingleOptionDescription(MAOptionDescriptionTest.TestProperties_of_MAOptionDescription):
    def get_description_instance_to_test(self):
        return MASingleOptionDescription()



class MASingleOptionDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToManyRelationDescription()

    # nothing special to test, reserved for the future
