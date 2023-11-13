from unittest import TestCase

from descriptions.MARelationDescription_class import MARelationDescription
from accessors.MAAccessor_class import MAAccessor
from accessors.MADictAccessor_class import MADictAccessor
from accessors.MANullAccessor_class import MANullAccessor
from descriptions.MAContainer_class import MAContainer
from descriptions.tests.MAReferenceDescriptionTest import TestProperties_of_MAReferenceDescription


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
