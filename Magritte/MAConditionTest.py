from unittest import TestCase

from MACondition import MACondition

class MACondition_generator_Test(TestCase):

    def test_gt(self):
        condition = MACondition.model > 5
        self.assertTrue(condition(7))
        self.assertFalse(condition(3))

    def test_lt(self):
        condition = MACondition.model < 5
        self.assertFalse(condition(7))
        self.assertTrue(condition(3))

    def test_ge(self):
        condition = MACondition.model >= 5
        self.assertTrue(condition(7))
        self.assertTrue(condition(5))
        self.assertFalse(condition(3))

    def test_le(self):
        condition = MACondition.model <= 5
        self.assertFalse(condition(7))
        self.assertTrue(condition(5))
        self.assertTrue(condition(3))

    def test_eq(self):
        condition = (MACondition.model == "foo")
        self.assertTrue(condition("foo"))
        self.assertFalse(condition("bar"))

    def test_ne(self):
        condition = (MACondition.model != "bar")
        self.assertTrue(condition("foo"))
        self.assertFalse(condition("bar"))



    def test_isEmpty(self):
        condition = MACondition.list.isEmpty()
        self.assertTrue(condition([]))
        self.assertFalse(condition(["foo", "bar"]))

    def test_notEmpty(self):
        condition = MACondition.list.notEmpty()
        self.assertFalse(condition([]))
        self.assertTrue(condition(["foo", "bar"]))

    def test_notEmpty(self):
        condition = MACondition.list.contains("foo")
        self.assertTrue(condition(["foo", "bar"]))
        self.assertFalse(condition(["bar", "delta"]))
