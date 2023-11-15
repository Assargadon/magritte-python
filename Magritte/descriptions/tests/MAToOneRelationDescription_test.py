from unittest import TestCase

from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.tests.MARelationDescription_test import TestProperties_of_MARelationDescription


class TestProperties_of_MAToOneRelationDescription(TestProperties_of_MARelationDescription):
    def get_description_instance_to_test(self):
        return MAToOneRelationDescription()



class MAToOneRelationDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToOneRelationDescription()
        self.nonNullInstance = "Non-null string"

    def test_validateKind(self):
        with self.subTest("no classes set - should always pass"):
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateKind(None)) == 0)
            self.assertTrue(len(self.desc._validateKind(36)) == 0)

        with self.subTest("classes set to str"):
            self.desc.classes = {str}
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateKind(None)) == 1)
            self.assertTrue(len(self.desc._validateKind(36)) == 1)

        with self.subTest("classes set to int"):
            self.desc.classes = {int}
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 1)
            self.assertTrue(len(self.desc._validateKind(None)) == 1)
            self.assertTrue(len(self.desc._validateKind(36)) == 0)
