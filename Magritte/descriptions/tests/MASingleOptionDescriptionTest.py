from unittest import TestCase

from descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from accessors.MAAccessor_class import MAAccessor
from descriptions.tests.MAOptionDescriptionTest import TestProperties_of_MAOptionDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription


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
