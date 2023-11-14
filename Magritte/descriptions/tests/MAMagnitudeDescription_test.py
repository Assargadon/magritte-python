from unittest import TestCase
from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from Magritte.descriptions.tests.MAElementDescription_test import TestProperties_of_MAElementDescription

class TestProperties_of_MAMagnitudeDescription(TestProperties_of_MAElementDescription):

    def get_description_instance_to_test(self):
        return MAMagnitudeDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('max', None),
            ('min', None),
            ('rangeErrorMessage', str)
        }


class MAMagnitudeDescriptionTest(TestCase):

    def setUp(self):
        self.inst = MAMagnitudeDescription()


    def test_setMinMax(self):
        self.inst.setMinMax(1, 10)
        self.assertEqual(self.inst.min, 1)
        self.assertEqual(self.inst.max, 10)

    def test_isWithinRange(self):
        self.assertEqual(self.inst.isWithinRange(3), True)
        self.inst.setMinMax(3, 9)
        self.assertEqual(self.inst.isWithinRange(10), False)
        self.assertEqual(self.inst.isWithinRange(7), True)

    def test_getRangeErrorMessage_by_default(self):
        self.inst.setMinMax(321, 987)
        self.assertTrue('321' in self.inst.rangeErrorMessage and '987' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(321, None)
        self.assertTrue('321' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(None, 987)
        self.assertTrue('987' in self.inst.rangeErrorMessage)

        self.inst.setMinMax(None, None)
        self.assertIsNone(self.inst.rangeErrorMessage)


    def test_isSortable(self):
        self.assertEqual(self.inst.isSortable(), True)


class MAMagnitude_ValidationTest(TestCase):
    def setUp(self):
        self.desc = MAMagnitudeDescription()
    
    def test_validateSpecific(self):
        with self.subTest("No range"):
            self.assertTrue(len(self.desc._validateSpecific(5)) == 0, "No range set - no errors should be")
            
        with self.subTest("Full range"):
            self.desc.setMinMax(1, 10)
            self.assertTrue(len(self.desc._validateSpecific(5)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(1)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(10)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(0)) == 1, "Out of range (min) - error expected")
            self.assertTrue(len(self.desc._validateSpecific(11)) == 1, "Out of range (max) - error expected")

        with self.subTest("min-opened range"):
            self.desc.max = 10
            self.assertTrue(len(self.desc._validateSpecific(5)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(10)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(11)) == 1, "Out of range (max) - error expected")

        with self.subTest("max-open range"):
            self.desc.min = 1
            self.assertTrue(len(self.desc._validateSpecific(5)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(1)) == 0, "Within range - no errors should be")
            self.assertTrue(len(self.desc._validateSpecific(0)) == 1, "Out of range (min) - error expected")
