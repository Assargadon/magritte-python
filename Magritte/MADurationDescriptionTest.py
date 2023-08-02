from unittest import TestCase
from MADurationDescription_class import MADurationDescription
from datetime import timedelta


class MADurationDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADurationDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, timedelta)

    def test_label(self):
        self.assertEqual(self.inst1.label, 'Duration')
