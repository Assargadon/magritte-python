from unittest import TestCase
from Magritte.MAMagnitudeDescription_class import MAMagnitudeDescription


class MAMagnitudeDescriptionTest(TestCase):

    def setUp(self):
        self.inst = MAMagnitudeDescription()

    def test_getMax(self):
        self.assertEqual(self.inst.max, None)

    def test_setMax(self):
        self.inst.max = 10
        self.assertEqual(self.inst.max, 10)

    def test_getMin(self):
        self.assertEqual(self.inst.min, None)

    def test_setMin(self):
        self.inst.min = 1
        self.assertEqual(self.inst.min, 1)

    def test_setMinMax(self):
        self.inst.setMinMax(1, 10)
        self.assertEqual(self.inst.max, 10)

    def test_getRangeErrorMessage(self):
        self.inst.setMinMax(1, 10)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be between {1} and {10}')

        self.inst.setMinMax(1, None)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be above or equeal to {1}')

        self.inst.setMinMax(None, 10)
        self.assertEqual(self.inst.rangeErrorMessage, f'Input must be below or eqeal to {10}')

        self.inst.setMinMax(None, None)
        self.assertEqual(self.inst.rangeErrorMessage, None)

    def test_setRangeErrorMessage(self):
        self.inst.rangeErrorMessage = 'error'
        self.assertEqual(self.inst.rangeErrorMessage, 'error')

    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)

    def testisWithinRange(self):
        self.assertEqual(self.inst.isWithinRange(3), True)
        self.inst.setMinMax(3, 9)
        self.assertEqual(self.inst.isWithinRange(10), False)
        self.assertEqual(self.inst.isWithinRange(7), True)
