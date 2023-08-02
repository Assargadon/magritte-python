from unittest import TestCase
from MAIntDescription_class import MAIntDescription


class MAIntDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAIntDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, int)

    def test_label(self):
        self.assertEqual(self.inst1.label, 'int')
