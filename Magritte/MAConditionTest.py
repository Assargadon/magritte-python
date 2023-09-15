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

    def test_contains(self):
        condition = MACondition.list.contains("foo")
        self.assertTrue(condition(["foo", "bar"]))
        self.assertFalse(condition(["bar", "delta"]))


    def test_complicated_expression_not_supported(self): # MACondition is for easy generation of the simple common tests. In such cases, just use lambda-function
        # Mind that `and` and `&` is not a same operator.
        # `&`, technically, bitwise - and may be overwritten,
        # but `and` is logical - it cannot be overwritten (due to it not only calcualte the outcome, but also controls flow), but still may be blocked.
        # same for `or` and `|`, `not` and `~`

        with self.assertRaises(Exception):
                condition = (MACondition.model >= 5) and (MACondition.model <= 11.5)

        with self.assertRaises(Exception):
                condition = (MACondition.model >= 5) & (MACondition.model <= 11.5)

        with self.assertRaises(Exception):
                condition = (MACondition.model < 5) or (MACondition.model > 11.5)

        with self.assertRaises(Exception):
                condition = (MACondition.model < 5) | (MACondition.model > 11.5)

        with self.assertRaises(Exception):
                condition = not (MACondition.model == 5)

        with self.assertRaises(Exception):
                condition = ~(MACondition.model != 5)
