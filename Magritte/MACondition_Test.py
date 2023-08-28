from unittest import TestCase
from MACondition_class import MACondition


class MAConditionTest(TestCase):

    def test_selector(self):
        condition = MACondition.selector("is_integer") #такой метод есть у float
        self.assertTrue(condition.value(-1.0))
        self.assertFalse(condition.value(0.5))


    def test_selectorArgument(self):
        condition = MACondition.selectorArgument("__lt__", 5)
        self.assertTrue(condition.value(1))
        self.assertFalse(condition.value(5))
        
    def test_receiverSelector(self):
        condition = MACondition.selectorArgument(1, "__eq__")
        self.assertTrue(condition.value(1))
        self.assertFalse(condition.value(0))
        
