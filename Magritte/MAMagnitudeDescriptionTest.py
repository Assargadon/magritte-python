from unittest import TestCase
from MAMagnitudeDescription_class import MAMagnitudeDescription
import MAElementDescriptionTest

class TestProperties_of_MAMagnitudeDescription(MAElementDescriptionTest.TestProperties_of_MAElementDescription):

    def get_description_instance_to_test(self):
        return MAMagnitudeDescription()

    def _properties(self):
        #{**dict1, **dict2} is actually a merge of two dictionaries
        return {
            **super()._properties(),
            'max': None,
            'min': None,
            'rangeErrorMessage': str
        }


class MAMagnitudeDescriptionTest(TestCase):

    def setUp(self):
        self.inst = MAMagnitudeDescription()


    def test_setMinMax(self):
        self.inst.setMinMax(1, 10)
        self.assertEqual(self.inst.max, 10)

    def test_isWithinRange(self):
        self.assertEqual(self.inst.isWithinRange(3), True)
        self.inst.setMinMax(3, 9)
        self.assertEqual(self.inst.isWithinRange(10), False)
        self.assertEqual(self.inst.isWithinRange(7), True)

    def test_getRangeErrorMessage_by_default(self):
        self.inst.setMinMax(1, 10)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be between {1} and {10}')

        self.inst.setMinMax(1, None)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be above or equal to {1}')

        self.inst.setMinMax(None, 10)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be below or equal to {10}')

        self.inst.setMinMax(None, None)
        self.assertEqual(self.inst.rangeErrorMessage, None)


    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)

