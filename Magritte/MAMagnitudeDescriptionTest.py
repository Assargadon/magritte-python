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
            **{ 
                'max': None,
                'min': None,
                'rangeErrorMessage': str
            }
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
        self.inst.setMinMax(3, 9)
        self.assertTrue('3' in self.inst.rangeErrorMessage and '9' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(3, None)
        self.assertTrue('3' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(None, 9)
        self.assertTrue('9' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(None, None)
        self.assertEqual(self.inst.rangeErrorMessage, None)


    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)

