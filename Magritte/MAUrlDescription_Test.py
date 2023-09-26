from MAUrlDescription_class import MAUrlDescription
import MAElementDescriptionTest


class TestProperties_of_MAUrlDescription(MAElementDescriptionTest.TestProperties_of_MAElementDescription):

    def get_description_instance_to_test(self):
        return MAUrlDescription()