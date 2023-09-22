from unittest import TestCase
from MAToManyRelationDescription_class import MAToManyRelationDescription
import MARelationDescriptionTest
import MADescriptionTest
from errors.MARequiredError import MARequiredError


class TestProperties_of_MAToManyRelationDescription(MARelationDescriptionTest.TestProperties_of_MARelationDescription):
    def get_description_instance_to_test(self):
        return MAToManyRelationDescription()


class MAToMany_ValidationTest(MADescriptionTest.MADescription_ValidationTest):
    def setUp(self):
        self.desc = MAToManyRelationDescription()
        self.nonNullInstance = ["one", "two", "three"]
    
    def test_validateRequired(self):
        super().test_validateRequired()
        
        with self.subTest("empty collection - beRequired"):
            self.desc.beRequired()
            self.assertFalse(len(self.desc._validateRequired([])) == 0, "Empty collection should be treated as missing value by MAToManyRelationDescription with beRequired")
            self.assertIsInstance(self.desc._validateRequired([])[0], MARequiredError, "MAToManyRelationDescription with beRequired should emit MARequiredError for empty collection")
            
        with self.subTest("empty collection - beOptional"):
            self.desc.beOptional()
            self.assertTrue(len(self.desc._validateRequired([])) == 0, "Empty collection is a valid value for optional MAToManyRelationDescription")

    def test_validateKind(self):
        with self.subTest("no classes set - should always pass"):
            with self.assertRaises(TypeError):
                self.desc._validateKind(None)
            with self.assertRaises(TypeError):
                self.desc._validateKind(36)
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateKind([None])) == 0)
            self.assertTrue(len(self.desc._validateKind([36])) == 0)

        with self.subTest("classes set to str"):
            self.desc.classes = {str}
            with self.assertRaises(TypeError):
                self.desc._validateKind(None)
            with self.assertRaises(TypeError):
                self.desc._validateKind(36)
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateKind([None])) == 1)
            self.assertTrue(len(self.desc._validateKind([36])) == 1)

        with self.subTest("classes set to int"):
            self.desc.classes = {int}
            with self.assertRaises(TypeError):
                self.desc._validateKind(None)
            with self.assertRaises(TypeError):
                self.desc._validateKind(36)
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 1)
            self.assertTrue(len(self.desc._validateKind([None])) == 1)
            self.assertTrue(len(self.desc._validateKind([36])) == 0)


class MAToManyRelationDescriptionTest(TestCase):

    def setUp(self):
        self.desc = MAToManyRelationDescription()

    # nothing special to test, reserved for the future
