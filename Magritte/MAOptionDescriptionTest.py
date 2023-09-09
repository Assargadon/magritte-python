from unittest import TestCase
from MAOptionDescription_class import MAOptionDescription
import MAReferenceDescriptionTest


class TestProperties_of_MAOptionDescription(MAReferenceDescriptionTest.TestProperties_of_MAReferenceDescription):
    def get_description_instance_to_test(self):
        return MAOptionDescription()

    def _properties(self):
        #{**dict1, **dict2} is actually a merge of two dictionaries
        return {
            **super()._properties(),
            **{
                'extensible': bool,
                'sorted': bool,
                'options': list
            }
        }

    def _flag_properties(self):
        return [
            *super()._flag_properties(),
            *[
                ('extensible', 'beExtensible', 'beLimited', 'isExtensible'),
                ('sorted', 'beSorted', 'beUnsorted', 'isSorted'),
            ]
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
