from unittest import TestCase
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.tests.MAElementDescription_test import TestProperties_of_MAElementDescription


class TestProperties_of_MABooleanDescription(TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MABooleanDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('trueString', str),
            ('falseString', str),
        }


class MABooleanDescriptionTest(TestCase):

    def test_defaultStrings(self):
        self.assertTrue(len(MABooleanDescription.defaultTrueStrings()) > 1,
                         "MABooleanDescription should have defaultTrueStrings"
        )
        self.assertTrue(len(MABooleanDescription.defaultFalseStrings()) > 1, 
                        "MABooleanDescription should have defaultFalseStrings"
        )
