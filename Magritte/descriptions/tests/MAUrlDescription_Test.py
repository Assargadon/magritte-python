from descriptions.MAUrlDescription_class import MAUrlDescription
from descriptions.tests.MAElementDescriptionTest import TestProperties_of_MAElementDescription


class TestProperties_of_MAUrlDescription(TestProperties_of_MAElementDescription):

    def get_description_instance_to_test(self):
        return MAUrlDescription()