from unittest import TestCase
from Magritte.MAElementDescription_class import MAElementDescription


class MAElementDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAElementDescription()
        self.inst2 = MAElementDescription()


    def test_getDefault(self):
        self.assertEqual(self.inst1.default, None)

    def test_setDefault(self):
        self.inst2.default = 'anObject'
        self.assertEqual(self.inst2.default, 'anObject')
