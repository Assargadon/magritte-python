from MAMemoDescription_class import MAMemoDescription
import MAStringDescriptionTest


class TestProperties_of_MAMemoDescription(MAStringDescriptionTest.TestProperties_of_MAStringDescription):

    def get_description_instance_to_test(self):
        return MAMemoDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('lineCount', int)
        }