from unittest import TestCase
from MADescription_class import MADescription

class MADescriptionWithFieldAndReadonlyAttribute(MADescription):
    def __init__(self, **kwargs):
        self.id = 42
        super().__init__(**kwargs)
        
    @property
    def pi(self):
        return 3.1415
        


class MAPluggableAccessorTest(TestCase):

    def test_correct_init(self):
        description = MADescriptionWithFieldAndReadonlyAttribute(priority=10, id=13)
        self.assertEqual(description.priority, 10)
        self.assertEqual(description.id, 13)

        self.assertEqual(description.pi, 3.1415)

    def test_init_with_readonly_attribute(self):
        with self.assertRaises(AttributeError):
            description = MADescriptionWithFieldAndReadonlyAttribute(pi=4)

    def test_init_with_absent_attribute(self):
        with self.assertRaises(AttributeError):
            description = MADescriptionWithFieldAndReadonlyAttribute(e=2.71828)
