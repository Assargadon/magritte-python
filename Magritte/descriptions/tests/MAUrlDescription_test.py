from Magritte.descriptions.MAUrlDescription_class import MAUrlDescription
from Magritte.descriptions.tests.MAElementDescription_test import TestProperties_of_MAElementDescription


class TestProperties_of_MAUrlDescription(TestProperties_of_MAElementDescription):

    def get_description_instance_to_test(self):
        return MAUrlDescription()