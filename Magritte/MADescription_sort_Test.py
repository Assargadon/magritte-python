from unittest import TestCase
from MADescription_class import MADescription

class MADescription_sort_Test(TestCase):

    def setUp(self):
        self.description0 = MADescription() #priority expected to be zero by default
        self.description1 = MADescription(priority=10)
        self.description2 = MADescription(priority=20)
        

    def test_comparison(self):
        self.assertTrue(self.description1 < self.description2)
        self.assertFalse(self.description2 < self.description1)

    def test_sorting(self):
        list_of_descriptions = [self.description2, self.description1, self.description0]
        list_of_descriptions.sort();
        
        self.assertEqual(list_of_descriptions[0], self.description0)
        self.assertEqual(list_of_descriptions[1], self.description1)
        self.assertEqual(list_of_descriptions[2], self.description2)
        

