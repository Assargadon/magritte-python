from unittest import TestCase
from MADescription_class import MADescription
from MANullAccessor_class import MANullAccessor
from MAAccessor_class import MAAccessor

class TestProperties_of_MADescription(TestCase):
    properties = { 
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
        self.counter = 0
        print("setUp invoked!")

    def get_description_instance_to_test(self):
        return MADescription()


    def check_default_value(self, prop, prop_type):
        print(f"prop to test: {prop} of type: {prop_type}")
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
                self.setUp()
                self.check_default_value(prop, prop_type)
                self.setUp()
                self.check_read_write(prop, prop_type)
                self.setUp()
                self.check_assigning_null(prop)


class MADescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADescription()
        self.inst2 = MADescription()
        self.inst3 = MADescription()
        self.inst1['accessor'] = 3
        self.inst2['kindErrorMessage'] = 3
        self.accessorTrue = 'accessor'
        self.accessorFalse = 3

    def test_eq(self):
        self.assertEqual(self.inst1 == self.inst1, True)
        self.assertEqual(self.inst1 == self.inst2, False)

    def test_setitem_and_getitem(self):
        self.assertEqual(self.inst1['accessor'], 3)

    def test_contains(self):
        self.assertEqual(self.inst1.__contains__(self.accessorTrue), True)
        self.assertEqual(self.inst1.__contains__(self.accessorFalse), False)

    def test_get(self):
        self.assertEqual(self.inst1.get('accessor', 0), 3)
        self.assertEqual(self.inst1.get('property', 0), 0)

    def test_isKindDefined(self):
        self.inst1.kind = 123
        self.assertEqual(self.inst1.isKindDefined(), True)
        self.assertEqual(self.inst2.isKindDefined(), False)

    def test_isReadOnly(self):
        self.inst1.readOnly = True
        self.assertEqual(self.inst1.isReadOnly(), True)
        self.assertEqual(self.inst2.isReadOnly(), False)

    def test_beReadOnly(self):
        self.inst1.beReadOnly()
        self.assertEqual(self.inst1.readOnly, True)

    def test_beWriteable(self):
        self.inst1.beWriteable()
        self.assertEqual(self.inst1.readOnly, False)

    def test_isRequired(self):
        self.inst1.required = True
        self.assertEqual(self.inst1.isRequired(), True)
        self.assertEqual(self.inst2.isRequired(), False)

    def test_beRequired(self):
        self.inst1.beRequired()
        self.assertEqual(self.inst1.required, True)

    def test_beOptional(self):
        self.inst1.beOptional()
        self.assertEqual(self.inst1.required, False)

    def test_hasComment(self):
        self.assertEqual(self.inst1.hasComment(), False)
        self.inst1.comment = 'comment'
        self.assertEqual(self.inst1.hasComment(), True)

    def test_hasLabel(self):
        self.assertEqual(self.inst1.hasLabel(), False)
        self.inst1.label = 'label'
        self.assertEqual(self.inst1.hasLabel(), True)

    def test_isVisible(self):
        self.assertEqual(self.inst1.isVisible(), False)
        self.inst1.readOnly = True
        self.assertEqual(self.inst1.isVisible(), True)

    def test_beVisible(self):
        self.inst1.beVisible()
        self.assertEqual(self.inst1.isVisible(), True)

    def test_beHidden(self):
        self.inst1.beHidden()
        self.assertEqual(self.inst1.isVisible(), False)

    def test_undefined_default(self):
        self.assertIsInstance(self.inst1.undefined, str)

    def test_undefined_readWrite(self):
        self.inst1.undefined = 'no value'
        self.assertEqual(self.inst1.undefined, 'no value')
        
    def test_undefined_assignNone(self):
        self.inst1.undefined = None
        self.assertIsInstance(self.inst1.undefined, str, "After assigning None to .undefined it should be defaultUndefined, not None")

    def test_isAbstract(self):
        self.assertEqual(self.inst1.isAbstract(), True)

    def test_isSortable(self):
        self.assertEqual(self.inst1.isSortable(), False)
