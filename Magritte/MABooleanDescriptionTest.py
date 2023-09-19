from unittest import TestCase
from MABooleanDescription_class import MABooleanDescription
import MAElementDescriptionTest


class TestProperties_of_MABooleanDescription(MAElementDescriptionTest.TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MABooleanDescription()
    
    def _properties(self):
        return {
            **super()._properties(),
            'trueString': str,
            'falseString': str,
        }


class MABooleanDescriptionTest(TestCase):
    pass
