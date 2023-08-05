from unittest import TestCase
from MANumberDescription_class import MANumberDescription
import MAMagnitudeDescriptionTest

class TestProperties_of_MANumberDescription(MAMagnitudeDescriptionTest.TestProperties_of_MAMagnitudeDescription):

    def get_description_instance_to_test(self):
        return MANumberDescription()

#class MANumberDescriptionTest(TestCase):
#
#    def setUp(self):
#        self.desc = MANumberDescription()
