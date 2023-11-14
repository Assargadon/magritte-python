from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.tests.MADescription_test import TestProperties_of_MADescription


class TestProperties_of_MAElementDescription(TestProperties_of_MADescription):

    def get_description_instance_to_test(self):
        return MAElementDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('default', None)
        }
