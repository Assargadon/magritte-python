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
            'extensible': bool,
            'sorted': bool,
            'options': list
        }

    def _flag_properties(self):
        return [
            ('visible', 'beVisible', 'beHidden', 'isVisible'),
            ('readOnly', 'beReadOnly', 'beWriteable', 'isReadOnly'),
            ('required', 'beRequired', 'beOptional', 'isRequired'),
            ('extensible', 'beExtensible', 'beLimited', 'isExtensible'),
            ('sorted', 'beSorted', 'beUnsorted', 'isSorted')
        ]

    def _checkable_properties(self):
        return [
            ('kind', 'isKindDefined'),
            ('comment', 'hasComment'),
            ('label', 'hasLabel'),
            ('extensible', 'isExtensible'),
            ('sorted', 'isSorted')
        ]


class MAOptionDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAOptionDescription()

    def test_copy(self):
        self.assertEqual(self.inst1.__copy__(), self.inst1)

    def test_options(self):
        self.assertEqual(self.inst1.options, [])
        self.inst1.options = [1, 2, 3]
        self.assertEqual(self.inst1.options, [1, 2, 3])

    def test_extensible(self):
        self.assertFalse(self.inst1.extensible)
        self.inst1.extensible = True
        self.assertTrue(self.inst1.extensible)

    def test_beExtensible(self):
        self.inst1.beExtensible()
        self.assertTrue(self.inst1.extensible)

    def test_beLimited(self):
        self.inst1.beLimited()
        self.assertFalse(self.inst1.extensible)

    def test_isExtensible(self):
        self.assertFalse(self.inst1.extensible)

    def test_sorted(self):
        self.assertFalse(self.inst1.sorted)
        self.inst1.sorted = True
        self.assertTrue(self.inst1.sorted)

    def test_beSorted(self):
        self.inst1.beSorted()
        self.assertTrue(self.inst1.sorted)

    def test_beUnsorted(self):
        self.inst1.beUnsorted()
        self.assertFalse(self.inst1.sorted)

    def test_undefined(self):
        self.assertEqual(self.inst1.undefined, '')
        self.inst1.undefined = 'string'
        self.assertEqual(self.inst1.undefined, 'string')
        self.assertEqual(self.inst1.reference.undefined, 'string')
