from unittest import TestCase
import types

from Magritte.descriptions.MADescription_class import MADescription
from Magritte.accessors.MAAccessor_class import MAAccessor
from Magritte.visitors.MAValidatorVisitor_class import MAValidatorVisitor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.errors.MARequiredError import MARequiredError
from Magritte.MACondition import MACondition
from Magritte.visitors.MAStringWriterReader_visitors import MAStringReaderVisitor, MAStringWriterVisitor


class TestProperties_of_MADescription(TestCase):

    def get_test_value(self, prop_name):
        matching_properties = [value for name, value, *isNonNullAccepting in self.properties if name == prop_name]
        prop_type = matching_properties[0]
        
        if prop_type == type:
            return list # Just because `list` is type which always exists
        elif prop_type == str:
            return 'test_str'
        elif prop_type == bool:
            return True
        elif prop_type == int:
            return 42
        elif prop_name == 'conditions':
            return [(MACondition.model >= 5, 'custom label: >=5'), (MACondition.model == 36, 'custom label: ==36')]
        elif prop_type == list:
            return [1, 2, 3]
        elif prop_type == set:
            return {1, 2, 3}
        elif prop_type == MAAccessor:
            return MAAccessor()
        elif prop_type == type(MAValidatorVisitor):
            return MAValidatorVisitor
        elif prop_type == MAStringReaderVisitor:
            return MAStringReaderVisitor()
        elif prop_type == MAStringWriterVisitor:
            return MAStringWriterVisitor()
        elif prop_type == MADescription:
            return MADescription()
        elif prop_type == MAContainer:
            return MAContainer()
        elif prop_type is None:
            return {'meaning': 'object to read-write when no type check expected', 'true_meaning': 42}
        else:
            raise Exception(f"Unhandled type {prop_type} for property {prop_name}")

    def setUp(self):
        self.my_desc = self.get_description_instance_to_test()
        
    def get_description_instance_to_test(self):
        return MADescription()

# ====================================================================

    @property
    def properties(self):
        return self._properties()

    def _properties(self):
        # add True as third parameter to tuple if property has non-null-accepting behavior,
        # i.e. if assigning None to it forces it to re-init itself from default values,
        # (for most metadescriptor fields, None is valid value, and may be assigned and stored,
        # and lazy initilization happens if field was _read before initialization_)
        # Set this third parameter to the type of expected non-null-accepting


        return {
            ('kind', type),
            ('kindErrorMessage', str),
            ('accessor', MAAccessor),
            ('readOnly', bool),
            ('required', bool),
            ('undefinedValue', None),
            ('name', str),
            ('comment', str),
            ('group', str),
            ('label', str),
            ('priority', int),
            ('conditions', list, True),
            ('visible', bool),
            ('undefined', str, True),
            
            ('requiredErrorMessage', str),
            ('kindErrorMessage', str),
            ('multipleErrorsMessage', str),
            ('conflictErrorMessage', str),
            ('validator', type(MAValidatorVisitor)) #not very clean - but I don't know what to do it properly. Good solution is to pass _instance_, not class
        }




    def check_default_value(self, prop, prop_type):
        default_val = getattr(self.my_desc, prop)
        if prop_type is None:
            # No type check is required; only ensuring that reading does not crash
            return
        if default_val is not None:
            self.assertIsInstance(default_val, prop_type, f'"{prop}" default value type is not as expected')
        else:
            # If the default value is None, this is acceptable as all default values are nullable
            pass

    def check_read_write(self, prop, prop_type):
        new_val = self.get_test_value(prop)
        setattr(self.my_desc, prop, new_val)
        actual_val = getattr(self.my_desc, prop)
        self.assertEqual(actual_val, new_val, f'"{prop}" did not update correctly')

    def check_assigning_null_to_common_field(self, prop):
    # If default value is _also_ None, this check may generate false positive
    # This false positive, however, does not affect the functioning (None will be returned, even if by wrong branch)
        setattr(self.my_desc, prop, None)
        actual_val = getattr(self.my_desc, prop)
        self.assertIsNone(actual_val, f'"{prop}" did not correctly accept None value')

    def check_assigning_null_to_non_null_accepting_field(self, prop, prop_type):
        # non-null-accepting fields are fields which has special behavior:
        # assigning None to them make them "non initialized", and they re-initialize themselves by default values
        setattr(self.my_desc, prop, None)
        self.check_default_value(prop, prop_type)

    def test_properties(self):
        for prop, prop_type, *isNonNullAccepting in self.properties:
            with self.subTest(property=prop, type=prop_type):
                # print(f"{prop} => {prop_type}")
                self.setUp()
                self.check_default_value(prop, prop_type)
                
                self.setUp()
                self.check_read_write(prop, prop_type)
                
                self.setUp()
                if isNonNullAccepting:
                    self.check_assigning_null_to_non_null_accepting_field(prop, prop_type)
                else:
                    self.check_assigning_null_to_common_field(prop)

# ====================================================================

    @property
    def flag_properties(self):
        return self._flag_properties()

    def _flag_properties(self):
        return [
            ('visible', 'beVisible', 'beHidden', 'isVisible'),
            ('readOnly', 'beReadOnly', 'beWriteable', 'isReadOnly'),
            ('required', 'beRequired', 'beOptional', 'isRequired'),
        ]
    
    def check_flag_property(self, prop, set_true, set_false, test):
        # Test setting to True via set_true method
        getattr(self.my_desc, set_true)()
        self.assertTrue(getattr(self.my_desc, prop), f"'{set_true}' did not set '{prop}' to True correctly")

        # Test setting to False via set_false method
        getattr(self.my_desc, set_false)()
        self.assertFalse(getattr(self.my_desc, prop), f"'{set_false}' did not set '{prop}' to False correctly")

        # Test proper retrieval via `test` method (True)
        setattr(self.my_desc, prop, True)
        self.assertTrue(getattr(self.my_desc, test)(), f"'{test}' did not return True correctly")

        # Test proper retrieval via `test` method (False)
        setattr(self.my_desc, prop, False)
        self.assertFalse(getattr(self.my_desc, test)(), f"'{test}' did not return False correctly")

    def test_flag_properties(self):
        for prop_tuple in self.flag_properties:
            with self.subTest(property=prop_tuple[0]):
                # print(f"flag: {prop_tuple}")
                self.setUp()
                self.check_flag_property(*prop_tuple)


# ====================================================================

    @property
    def checkable_properties(self):
        return self._checkable_properties()

    def _checkable_properties(self):
        return [
            ('kind', 'isKindDefined'),
            ('comment', 'hasComment'),
            ('label', 'hasLabel')
        ]

    def check_property_defined(self, prop, check_method):
        # Check if the property is initially reported as not defined
        self.assertFalse(getattr(self.my_desc, check_method)(), f"'{check_method}' should return False when '{prop}' is not set")

        # Assign a value to the property
        new_val = self.get_test_value(prop) # Assuming `self.properties` has the type info
        setattr(self.my_desc, prop, new_val)

        # Check if the property is now reported as defined
        self.assertTrue(getattr(self.my_desc, check_method)(), f"'{check_method}' should return True when '{prop}' is set")

    def test_checkable_properties(self):
        for prop_tuple in self.checkable_properties:
            with self.subTest(property=prop_tuple[0]):
                # print(f"checkable prop: {prop_tuple}")
                self.setUp()
                self.check_property_defined(*prop_tuple)


class MADescription_ValidationTest(TestCase):
    def setUp(self):
        self.desc = MADescription()
        self.nonNullInstance = "Some value - it may be both complex object and scalar value"

    def test_validateRequired(self):
        with self.subTest("optional"):
            self.desc.beOptional()
            self.assertTrue(len(self.desc._validateRequired(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateRequired(None)) == 0, "Description is optional, None should pass the test")
        
        with self.subTest("required"):
            self.desc.beRequired()
            self.assertTrue(len(self.desc._validateRequired(self.nonNullInstance)) == 0)
            self.assertFalse(len(self.desc._validateRequired(None)) == 0)
            self.assertIsInstance(self.desc._validateRequired(None)[0], MARequiredError)

    def test_validateKind(self):
        with self.subTest("kind is any object"):
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc._validateKind(None)) == 0)
            self.assertTrue(len(self.desc._validateKind(36)) == 0)

        with self.subTest("use a visitor"):
            self.assertTrue(len(self.desc.validate(self.nonNullInstance)) == 0)
            self.assertTrue(len(self.desc.validate(None)) == 0)
            self.assertTrue(len(self.desc.validate(36)) == 0)

        with self.subTest("kind is specific wrong class"):
            self.desc.kind = Exception
            self.assertTrue(len(self.desc._validateKind(self.nonNullInstance)) == 1)
            self.assertTrue(len(self.desc._validateKind(None)) == 1)
            self.assertTrue(len(self.desc._validateKind(36)) == 1)

        with self.subTest("use a visitor"):
            self.assertTrue(len(self.desc.validate(self.nonNullInstance)) == 1)
            self.assertTrue(len(self.desc.validate(None)) == 0)   # none is undefinedValue for description - no error
            self.assertTrue(len(self.desc.validate(36)) == 1)


class MADescriptionTest(TestCase):

    def setUp(self):
        self.desc1 = MADescription()
        self.desc2 = MADescription()



    def test_eq(self):
        self.assertEqual(self.desc1, self.desc1, "Equality check failed for comparing Description instance with itself")
        self.assertNotEqual(self.desc1, self.desc2, "Inequality check failed for comparing two independent description instances")



    def test_addCondition(self):
        self.assertEqual(len(self.desc1.conditions), 0)
        
        self.desc1.addCondition((lambda model: True), "always true")
        self.assertEqual(len(self.desc1.conditions), 1)
        self.assertIsInstance(self.desc1.conditions[0][0], types.LambdaType)
        self.assertEqual(self.desc1.conditions[0][1], "always true")
        
        self.desc1.addCondition((lambda model: False)) # label is ommited - None expected to be added as label
        self.assertEqual(len(self.desc1.conditions), 2)
        self.assertIsInstance(self.desc1.conditions[1][0], types.LambdaType)
        self.assertIsNone(self.desc1.conditions[1][1])

        self.desc1.addCondition(MACondition.model >= 5) #label is ommited, but MACondition generators have labels
        self.assertEqual(len(self.desc1.conditions), 3)
        self.assertIsInstance(self.desc1.conditions[2][0], MACondition)
        self.assertIsInstance(self.desc1.conditions[2][1], str)
        

    def test_conditionsConvertionOnAssignment(self):
        self.desc1.conditions = [MACondition.model >= 5, lambda x: x != 10, (MACondition.model == 36, "test custom label")]
        self.assertEqual(len(self.desc1.conditions), 3)

        self.assertIsInstance(self.desc1.conditions[0][0], MACondition)
        self.assertIsInstance(self.desc1.conditions[0][1], str)
        
        self.assertIsInstance(self.desc1.conditions[1][0], types.LambdaType)
        self.assertIsNone(self.desc1.conditions[1][1])
        
        self.assertIsInstance(self.desc1.conditions[2][0], MACondition)
        self.assertEqual(self.desc1.conditions[2][1], "test custom label")
        

    def test_validateConditions(self):
        self.assertEqual(len(self.desc1._validateConditions("test model")), 0, "Freshly initialized description with no conditions should return zero errors on `_validateConditions`")

        self.desc1.addCondition(lambda model: False, "Condition always fails")
        self.desc1.addCondition(lambda model: True, "Condition always met")
        self.assertEqual(len(self.desc1._validateConditions("test model")), 1, "One unmet condition is here")
        self.assertEqual(self.desc1._validateConditions("test model")[0].message, "Condition always fails")
        
    def test_isSortable(self):
        self.assertEqual(self.desc1.isSortable(), False)
