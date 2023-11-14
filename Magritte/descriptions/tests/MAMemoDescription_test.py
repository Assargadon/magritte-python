from Magritte.descriptions.MAMemoDescription_class import MAMemoDescription
from Magritte.descriptions.tests.MAStringDescription_test import TestProperties_of_MAStringDescription


class TestProperties_of_MAMemoDescription(TestProperties_of_MAStringDescription):

    def get_description_instance_to_test(self):
        return MAMemoDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('lineCount', int)
        }