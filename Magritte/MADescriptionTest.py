from unittest import TestCase
from MADescription_class import MADescription
from MANullAccessor_class import MANullAccessor
from MAAccessor_class import MAAccessor

class TestProperties_of_MADescription(TestCase):

    def get_test_value(self, prop_name, prop_type):
        if prop_type == type:
            return list # Just because `list` is type which always exists
        elif prop_type == str:
            return 'test_str'
        elif prop_type == bool:
            return True
        elif prop_type == int:
            return 42
        elif prop_type == MAAccessor:
            return MAAccessor()
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
        return { 
            'kind': type,
            'kindErrorMessage': str,
            'accessor': MAAccessor,
            'readOnly': bool,
            'required': bool,
            'undefinedValue': None,
            'name': str,
            'comment': str,
            'group': str,
            'label': str,
            'priority': int,
            'visible': bool
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
        new_val = self.get_test_value(prop, prop_type)
        setattr(self.my_desc, prop, new_val)
        actual_val = getattr(self.my_desc, prop)
        self.assertEqual(actual_val, new_val, f'"{prop}" did not update correctly')

    def check_assigning_null(self, prop):
    # If default value is _also_ None, this check may generate false positive
    # This false positive, however, does not affect the functioning (None will be returned, even if by wrong branch)
        setattr(self.my_desc, prop, None)
        actual_val = getattr(self.my_desc, prop)
        self.assertIsNone(actual_val, f'"{prop}" did not correctly accept None value')

    def test_properties(self):
        for prop, prop_type in self.properties.items():
            with self.subTest(property=prop, type=prop_type):
                # print(f"{prop} => {prop_type}")
                self.setUp()
                self.check_default_value(prop, prop_type)
                self.setUp()
                self.check_read_write(prop, prop_type)
                self.setUp()
                self.check_assigning_null(prop)

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
        new_val = self.get_test_value(prop, self.properties[prop]) # Assuming `self.properties` has the type info
        setattr(self.my_desc, prop, new_val)

        # Check if the property is now reported as defined
        self.assertTrue(getattr(self.my_desc, check_method)(), f"'{check_method}' should return True when '{prop}' is set")

    def test_checkable_properties(self):
        for prop_tuple in self.checkable_properties:
            with self.subTest(property=prop_tuple[0]):
                # print(f"checkable prop: {prop_tuple}")
                self.setUp()
                self.check_property_defined(*prop_tuple)


class MADescriptionTest(TestCase):

    def setUp(self):
        self.desc1 = MADescription()
        self.desc2 = MADescription()



    def test_eq(self):
        self.assertEqual(self.desc1, self.desc1, "Equality check failed for comparing Description instance with itself")
        self.assertNotEqual(self.desc1, self.desc2, "Inequality check failed for comparing two independent description instances")

    def test_setitem_and_getitem(self):
        self.desc1.id = 13
        self.assertEqual(self.desc1.id, 13, "Failed to set or retrieve the value using item access")

    def test_in(self):
        self.desc1.fieldname = {'meaning': 'some object just to assign a value (because something like `3` is not explanatory)'}
        self.assertTrue("fieldname" in self.desc1.__dict__, "Field 'fieldname' WAS assigned, and therefore should be `in` desc1, but it was not found")
        self.assertFalse("fieldname" in self.desc2.__dict__, "Field 'fieldname' was NOT assigned, and therefore it should NOT be `in` desc2, but it was found")

    def test_get(self):
        self.desc1.id = 13
        self.assertEqual(self.desc1.id, 13, "`.get` method failed to retrieve assigned value for 'id'")
        #self.assertEqual(self.desc2.get('id', -7), -7, "`.get` method did not return the default value when 'id' was not found")



    def test_undefined_default(self):
        self.assertIsInstance(self.desc1.undefined, str)

    def test_undefined_readWrite(self):
        self.desc1.undefined = 'no value'
        self.assertEqual(self.desc1.undefined, 'no value')
        
    def test_undefined_assignNone(self):
        self.desc1.undefined = None
        self.assertIsInstance(self.desc1.undefined, str, "After assigning None to .undefined it should be defaultUndefined, not None")



    def test_isAbstract(self):
        self.assertEqual(self.desc1.isAbstract(), True)

    def test_isSortable(self):
        self.assertEqual(self.desc1.isSortable(), False)
