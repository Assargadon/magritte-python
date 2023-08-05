from unittest import TestCase
from MAFloatDescription_class import MAFloatDescription


class MAFloatDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAFloatDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, float)

    def test_label(self):
        self.assertEqual(self.inst1.label, 'float')