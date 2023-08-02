from unittest import TestCase
from MADateAndTimeDescription_class import MADateAndTimeDescription
from datetime import datetime


class MADateAndTimeDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADateAndTimeDescription()

    def test_kind(self):
        self.assertEqual(self.inst1.kind, datetime)

    def test_label(self):
        self.assertEqual(self.inst1.label, 'Date and Time')
