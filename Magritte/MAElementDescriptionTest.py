from MAElementDescription_class import MAElementDescription
import MADescriptionTest

class TestProperties_of_MAElementDescription(MADescriptionTest.TestProperties_of_MADescription):

    def get_description_instance_to_test(self):
        return MAElementDescription()

    def _properties(self):
        #{**dict1, **dict2} is actually a merge of two dictionaries
        return {
            **super()._properties(),
            **{ 
                'default': None
            }
        }
