from unittest import TestCase

from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.accessors.MAAccessor_class import MAAccessor
from Magritte.accessors.MADictAccessor_class import MADictAccessor
from Magritte.accessors.MANullAccessor_class import MANullAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.tests.MAReferenceDescription_test import TestProperties_of_MAReferenceDescription


class TestProperties_of_MARelationDescription(TestProperties_of_MAReferenceDescription):
    def get_description_instance_to_test(self):
        return MARelationDescription()

    def _properties(self):
        return {
            *super()._properties(),
            ('classes', set)
        }


class MARelationDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MARelationDescription()

    def test_copy(self):
        self.assertEqual(self.inst1.__copy__(), self.inst1)

    def test_commonClass(self):	
        self.assertIsNone(self.inst1.commonClass())

        self.inst1.classes = [MADictAccessor, MAAccessor, MANullAccessor]
        self.assertEqual(self.inst1.commonClass(), MAAccessor)

    def test_reference(self):
        self.assertIsInstance(self.inst1.reference, MAContainer)
