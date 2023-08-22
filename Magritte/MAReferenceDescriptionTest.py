from unittest import TestCase
from MAReferenceDescription_class import MAReferenceDescription
from MAStringDescription_class import MAStringDescription
from MADescription_class import MADescription
import MAStringDescriptionTest


class TestProperties_of_MAReferenceDescription(MAStringDescriptionTest.TestProperties_of_MAStringDescription):
    def get_description_instance_to_test(self):
        return MAReferenceDescription()

    def _properties(self):
        #{**dict1, **dict2} is actually a merge of two dictionaries
        return {
            **super()._properties(),
            **{
                'initializer': MADescription,
                'reference': MADescription
            }
        }


class MAReferenceDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAReferenceDescription()

    def test_copy(self):
        copy_test = self.inst1.__copy__()
        self.assertEqual(copy_test, self.inst1)

    def test_initializer(self):
        self.assertEqual(self.inst1.initializer, self.inst1)
        self.inst1.initializer = 123
        self.assertEqual(self.inst1.initializer, 123)

    def test_reference(self):
        self.assertIsInstance(self.inst1.reference, MAStringDescription)
        self.inst1.reference = [1, 2, 3]
        self.assertEqual(self.inst1.reference, [1, 2, 3])
