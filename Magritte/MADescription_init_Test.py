from unittest import TestCase
from MADescription_class import MADescription

class MADescriptionWithReadonlyAttribute(MADescription):
        
    @property
    def pi(self):
        return 3.1415
        


class MADescription_init_Test(TestCase):

    def test_correct_init(self):
        description = MADescriptionWithReadonlyAttribute(priority=10, label="TestField")
        self.assertEqual(description.priority, 10)
        self.assertEqual(description.label, "TestField")

    def test_init_with_readonly_attribute(self):
        with self.assertRaises(AttributeError):
            description = MADescriptionWithReadonlyAttribute(pi=4)

    def test_init_with_absent_attribute(self):
        with self.assertRaises(AttributeError):
            description = MADescriptionWithReadonlyAttribute(e=2.71828)
