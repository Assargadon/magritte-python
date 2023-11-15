from unittest import TestCase

from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.accessors.MAAccessor_class import MAAccessor
from Magritte.descriptions.tests.MAOptionDescription_test import TestProperties_of_MAOptionDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription


class TestProperties_of_MASingleOptionDescription(TestProperties_of_MAOptionDescription):
    def get_description_instance_to_test(self):
        return MASingleOptionDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('groupBy', MAAccessor)
        }
        
    def _checkable_properties(self):
        return [
            *super()._checkable_properties(),
            ('groupBy', 'isGrouped')
        ]

class MASingleOptionDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToManyRelationDescription()

    # nothing special to test, reserved for the future
