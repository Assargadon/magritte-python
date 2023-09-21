from unittest import TestCase
from MAReferenceDescription_class import MAReferenceDescription
from MAStringDescription_class import MAStringDescription
from MADescription_class import MADescription
import MAElementDescriptionTest


class TestProperties_of_MAReferenceDescription(MAElementDescriptionTest.TestProperties_of_MAElementDescription):
    def get_description_instance_to_test(self):
        return MAReferenceDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('reference', MADescription, True)
        }

class MAReferenceDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAReferenceDescription()

    def test_copy(self):
        copy_test = self.inst1.__copy__()
        self.assertEqual(copy_test, self.inst1)
