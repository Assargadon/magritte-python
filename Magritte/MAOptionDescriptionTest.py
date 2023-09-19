from unittest import TestCase
from MAOptionDescription_class import MAOptionDescription
import MAReferenceDescriptionTest
from accessors.MAAccessor_class import MAAccessor

class TestProperties_of_MAOptionDescription(MAReferenceDescriptionTest.TestProperties_of_MAReferenceDescription):
    def get_description_instance_to_test(self):
        return MAOptionDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('extensible', bool),
            ('sorted', bool),
            ('options', list),
            ('groupBy', MAAccessor)
        }

    def _flag_properties(self):
        return [
            *super()._flag_properties(),
            *[
                ('extensible', 'beExtensible', 'beLimited', 'isExtensible'),
                ('sorted', 'beSorted', 'beUnsorted', 'isSorted'),
            ]
        ]

    def _checkable_properties(self):
        return [
            *super()._checkable_properties(),
            ('groupBy', 'isGrouped')
        ]


class MAOptionDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAOptionDescription()

    def test_copy(self):
        self.assertEqual(self.inst1.__copy__(), self.inst1)

    def test_undefined(self):
        self.assertEqual(self.inst1.undefined, '')
        self.inst1.undefined = 'string'
        self.assertEqual(self.inst1.undefined, 'string')
        self.assertEqual(self.inst1.reference.undefined, 'string')
