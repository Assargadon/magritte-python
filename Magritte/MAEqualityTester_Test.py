from datetime import datetime
from unittest import TestCase

from typing import List

from MAContainer_class import MAContainer
from MADateAndTimeDescription_class import MADateAndTimeDescription
from MAFloatDescription_class import MAFloatDescription
from MAOptionDescription_class import MAOptionDescription
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAToOneRelationDescription_class import MAToOneRelationDescription
from accessors.MAIdentityAccessor_class import MAIdentityAccessor
from MAIntDescription_class import MAIntDescription
from MAStringDescription_class import MAStringDescription
from MAEqualityTester_visitor import MAEqualityTester


class TestObject1:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class TestObject2:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_object: TestObject1):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_object = ref_object


class TestObject3:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_objects: List[TestObject1]):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_objects = ref_objects


class TestGlossary:
    def __init__(self, name: str):
        self.name = name


class TestObject4:
    def __init__(self, name: str, selection: TestGlossary):
        self.name = name
        self.selection = selection


class TestObject5:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_object: "TestObject5" = None):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_object = ref_object


class TestObject6:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_object: "TestObject7" = None):
        self.name = name
        self.ref_object = ref_object
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class TestObject7:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime, ref_object: TestObject6 = None):
        self.name = name
        self.ref_object = ref_object
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class TestObject8_1:
    def __init__(self, name: str, int_val: int, ref_object: "TestObject8_2" = None):
        self.name = name
        self.ref_object = ref_object
        self.int_value = int_val


class TestObject8_2:
    def __init__(self, name: str, int_val: int, ref_object: "TestObject8_3" = None):
        self.name = name
        self.ref_object = ref_object
        self.int_value = int_val


class TestObject8_3:
    def __init__(self, name: str, int_val: int, ref_object: TestObject8_1 = None):
        self.name = name
        self.ref_object = ref_object
        self.int_value = int_val


class MAEqualityTester_Test(TestCase):
    def setUp(self):
        # ==================== Encoders for testing. ====================
        self.equality_tester = MAEqualityTester()
        self.time_now = datetime.now()

        # ==================== Scalar values testing. ====================
        self.int_desc = MAIntDescription(name='TestInt', label='Test Int', default=0, accessor=MAIdentityAccessor())
        self.int_value = 123
        self.int_value_equal = 123
        self.int_value_not_equal = 234

        self.str_desc = MAStringDescription(
            name='TestString', label='Test String', default='',
            accessor=MAIdentityAccessor()
            )
        self.str_value = 'abc'
        self.str_value_equal = 'abc'
        self.str_value_not_equal = 'def'

        self.float_desc = MAFloatDescription(
            name='TestFloat', label='Test Float', default=0.0,
            accessor=MAIdentityAccessor()
            )
        self.float_value = 1.23
        self.float_value_equal = 1.23
        self.float_value_not_equal = 2.34

        self.date_desc = MADateAndTimeDescription(
            name='TestDate', label='Test Date', default=self.time_now, accessor=MAIdentityAccessor()
            )
        self.date_value = self.time_now
        self.date_value_equal = self.time_now
        self.date_value_not_equal = datetime.now()

        # ==================== Scalar relation value testing. ====================
        self.scalar_rel_desc = MAToOneRelationDescription(
            name='TestScalarRel', label='Test Scalar Relation', accessor=MAIdentityAccessor(), reference=self.int_desc
            )
        self.scalar_rel_value = self.int_value
        self.scalar_rel_value_equal = self.int_value
        self.scalar_rel_value_not_equal = self.int_value_not_equal

        # ==================== Object encoding testing. ====================
        self.object_desc = MAContainer()
        self.object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.object1 = TestObject1('object1', 123, 1.23, self.time_now)
        self.object1_equal = TestObject1('object1', 123, 1.23, self.time_now)
        self.object2 = TestObject1('object2', 234, 2.34, self.time_now)
        self.object1_not_equal = self.object2

        # ==================== Compound object with to-one relation testing. ====================
        self.compound_object_desc = MAContainer()
        self.compound_object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object_desc
                    ),
                ]
            )
        self.compound_object_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.compound_object_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.compound_object = TestObject2('object3', 345, 3.45, self.time_now, self.object1)
        self.compound_object_equal = TestObject2('object3', 345, 3.45, self.time_now, self.object1_equal)
        self.compound_object_not_equal = TestObject2('object3', 345, 3.45, self.time_now, self.object1_not_equal)

        # ==================== Compound object with to-many relation testing. ====================
        self.compound_object2_desc = MAContainer()
        self.compound_object2_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                MAToManyRelationDescription(
                    label='Referenced Objects', accessor='ref_objects', reference=self.object_desc
                    ),
                ]
            )
        self.compound_object2_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.compound_object2_desc_alt.setChildren(
            [
                MAToManyRelationDescription(
                    label='Referenced Objects', accessor='ref_objects', reference=self.object_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.compound_object2 = TestObject3(
            'object4', 456, 4.56, self.time_now, [self.object1, self.object2]
            )
        self.compound_object2_equal = TestObject3(
            'object4', 456, 4.56, self.time_now, [self.object1_equal, self.object2]
            )
        self.compound_object2_equal2 = TestObject3(
            'object4', 456, 4.56, self.time_now, [self.object2, self.object1_equal]
            )
        self.compound_object2_not_equal = TestObject3(
            'object4', 456, 4.56, self.time_now, [self.object1_not_equal, self.object2]
            )

        # ==================== Object with option testing. ====================
        self.glossary_desc = MAContainer()
        self.glossary_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                ]
            )
        self.glossary1 = TestGlossary('glossary1')
        self.glossary1_equal = TestGlossary('glossary1')
        self.glossary2 = TestGlossary('glossary2')
        self.glossary1_not_equal = self.glossary2

        self.object4_desc = MAContainer()
        self.object4_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAOptionDescription(
                    label='Selection', accessor='selection', reference=self.glossary_desc,
                    options=[self.glossary1, self.glossary2]
                    ),
                ]
            )
        self.object4_desc_alt = MAContainer()  # alternative object description: option coming first
        self.object4_desc_alt.setChildren(
            [
                MAOptionDescription(
                    label='Selection', accessor='selection', reference=self.glossary_desc,
                    options=[self.glossary1, self.glossary2]
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                ]
            )
        self.object4 = TestObject4('object4', self.glossary1)
        self.object4_equal = TestObject4('object4', self.glossary1_equal)
        self.object4_not_equal = TestObject4('object4', self.glossary1_not_equal)

        # ==================== Object with to-one relation to itself testing. ====================
        self.object5_desc = MAContainer()
        self.object5_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object5_desc
                    ),
                ]
            )
        self.object5_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object5_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object5_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.object5 = TestObject5('object5', 567, 5.67, self.time_now)
        self.object5.ref_object = self.object5
        self.object5_equal = TestObject5('object5', 567, 5.67, self.time_now)
        self.object5_equal.ref_object = self.object5_equal
        self.object5_not_equal = TestObject5('object5', 567, 5.67, self.time_now)

        # ==================== Two objects with cyclic cross-references. ====================
        self.object6_desc = MAContainer()
        self.object7_desc = MAContainer()
        self.object6_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object7_desc
                    ),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.object7_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object6_desc
                    ),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.object6_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object7_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object6_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object7_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )
        self.object7_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object6_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )

        self.object6 = TestObject6('object6', 678, 6.78, self.time_now)
        self.object7 = TestObject7('object7', 678, 6.78, self.time_now)
        self.object6.ref_object = self.object7
        self.object7.ref_object = self.object6
        self.object6_equal = TestObject6('object6', 678, 6.78, self.time_now)
        self.object7_equal = TestObject7('object7', 678, 6.78, self.time_now)
        self.object6_equal.ref_object = self.object7_equal
        self.object7_equal.ref_object = self.object6_equal
        self.object6_not_equal = TestObject6('object6', 678, 6.78, self.time_now)
        self.object7_not_equal = TestObject7('object7', 678, 6.78, self.time_now)
        self.object6_not_equal.ref_object = self.object7_not_equal
        self.object7_not_equal.ref_object = self.object7

    # ==================== Three objects with cyclic cross-references. ====================
        self.object8_1_desc = MAContainer()
        self.object8_2_desc = MAContainer()
        self.object8_3_desc = MAContainer()
        self.object8_1_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_2_desc
                    ),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )
        self.object8_2_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_3_desc
                    ),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )
        self.object8_3_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_1_desc
                    ),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )
        self.object8_1_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object8_2_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object8_3_desc_alt = MAContainer()  # alternative object description: reference coming first
        self.object8_1_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_2_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )
        self.object8_2_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_3_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )
        self.object8_3_desc_alt.setChildren(
            [
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object8_1_desc
                    ),
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                ]
            )

        self.object8_1 = TestObject8_1('object8_1', 789, None)
        self.object8_2 = TestObject8_2('object8_2', 890, None)
        self.object8_3 = TestObject8_3('object8_3', 901, None)
        self.object8_1.ref_object = self.object8_2
        self.object8_2.ref_object = self.object8_3
        self.object8_3.ref_object = self.object8_1
        self.object8_1_equal = TestObject8_1('object8_1', 789, None)
        self.object8_2_equal = TestObject8_2('object8_2', 890, None)
        self.object8_3_equal = TestObject8_3('object8_3', 901, None)
        self.object8_1_equal.ref_object = self.object8_2_equal
        self.object8_2_equal.ref_object = self.object8_3_equal
        self.object8_3_equal.ref_object = self.object8_1_equal
        self.object8_1_not_equal = TestObject8_1('object8_1', 789, None)
        self.object8_2_not_equal = TestObject8_2('object8_2', 890, None)
        self.object8_3_not_equal = TestObject8_3('object8_3', 902, None)  # change in int_value
        self.object8_1_not_equal.ref_object = self.object8_2_not_equal
        self.object8_2_not_equal.ref_object = self.object8_3_not_equal
        self.object8_3_not_equal.ref_object = self.object8_1_not_equal
        # difference in the deepest nested reference:
        self.object8_1_not_equal2 = TestObject8_1('object8_1', 789, None)
        self.object8_2_not_equal2 = TestObject8_2('object8_2', 890, None)
        self.object8_3_not_equal2 = TestObject8_3('object8_3', 901, None)
        self.object8_1_not_equal2.ref_object = self.object8_2_not_equal2
        self.object8_2_not_equal2.ref_object = self.object8_3_not_equal2
        self.object8_3_not_equal2.ref_object = self.object8_1_not_equal  # reference to "foreign" object8_2_not_equal

    def test_int_equality(self):
        self.assertTrue(self.equality_tester.equal(self.int_value, self.int_value_equal, self.int_desc))
        self.assertFalse(self.equality_tester.equal(self.int_value, self.int_value_not_equal, self.int_desc))

    def test_str_equality(self):
        self.assertTrue(self.equality_tester.equal(self.str_value, self.str_value_equal, self.str_desc))
        self.assertFalse(self.equality_tester.equal(self.str_value, self.str_value_not_equal, self.str_desc))

    def test_float_equality(self):
        self.assertTrue(self.equality_tester.equal(self.float_value, self.float_value_equal, self.float_desc))
        self.assertFalse(self.equality_tester.equal(self.float_value, self.float_value_not_equal, self.float_desc))

    def test_date_equality(self):
        self.assertTrue(self.equality_tester.equal(self.date_value, self.date_value_equal, self.date_desc))
        self.assertFalse(self.equality_tester.equal(self.date_value, self.date_value_not_equal, self.date_desc))

    def test_scalar_rel_equality(self):
        self.assertTrue(
            self.equality_tester.equal(self.scalar_rel_value, self.scalar_rel_value_equal, self.scalar_rel_desc)
            )
        self.assertFalse(
            self.equality_tester.equal(self.scalar_rel_value, self.scalar_rel_value_not_equal, self.scalar_rel_desc)
            )

    def test_object_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object1, self.object1_equal, self.object_desc))
        self.assertFalse(self.equality_tester.equal(self.object1, self.object1_not_equal, self.object_desc))

    def test_compound_object_equality(self):
        self.assertTrue(
            self.equality_tester.equal(self.compound_object, self.compound_object_equal, self.compound_object_desc)
            )
        self.assertFalse(
            self.equality_tester.equal(self.compound_object, self.compound_object_not_equal, self.compound_object_desc)
            )
        self.assertTrue(
            self.equality_tester.equal(self.compound_object, self.compound_object_equal, self.compound_object_desc_alt)
            )
        self.assertFalse(
            self.equality_tester.equal(self.compound_object, self.compound_object_not_equal, self.compound_object_desc_alt)
            )

    def test_compound_object2_equality(self):
        self.assertTrue(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_equal, self.compound_object2_desc)
            )
        self.assertTrue(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_equal2, self.compound_object2_desc)
            )
        self.assertFalse(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_not_equal, self.compound_object2_desc)
            )
        self.assertTrue(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_equal, self.compound_object2_desc_alt)
            )
        self.assertTrue(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_equal2, self.compound_object2_desc_alt)
            )
        self.assertFalse(
            self.equality_tester.equal(self.compound_object2, self.compound_object2_not_equal, self.compound_object2_desc_alt)
            )

    def test_object4_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object4, self.object4_equal, self.object4_desc))
        self.assertFalse(self.equality_tester.equal(self.object4, self.object4_not_equal, self.object4_desc))
        self.assertTrue(self.equality_tester.equal(self.object4, self.object4_equal, self.object4_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object4, self.object4_not_equal, self.object4_desc_alt))

    def test_object5_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object5, self.object5_equal, self.object5_desc))
        self.assertFalse(self.equality_tester.equal(self.object5, self.object5_not_equal, self.object5_desc))
        self.assertTrue(self.equality_tester.equal(self.object5, self.object5_equal, self.object5_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object5, self.object5_not_equal, self.object5_desc_alt))

    def test_object6_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object6, self.object6_equal, self.object6_desc))
        self.assertFalse(self.equality_tester.equal(self.object6, self.object6_not_equal, self.object6_desc))
        self.assertTrue(self.equality_tester.equal(self.object6, self.object6_equal, self.object6_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object6, self.object6_not_equal, self.object6_desc_alt))

    def test_object7_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object7, self.object7_equal, self.object7_desc))
        self.assertFalse(self.equality_tester.equal(self.object7, self.object7_not_equal, self.object7_desc))
        self.assertTrue(self.equality_tester.equal(self.object7, self.object7_equal, self.object7_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object7, self.object7_not_equal, self.object7_desc_alt))

    def test_object8_equality(self):
        self.assertTrue(self.equality_tester.equal(self.object8_1, self.object8_1_equal, self.object8_1_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_1, self.object8_1_not_equal, self.object8_1_desc))
        self.assertTrue(self.equality_tester.equal(self.object8_1, self.object8_1_equal, self.object8_1_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_1, self.object8_1_not_equal, self.object8_1_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_1, self.object8_1_not_equal2, self.object8_1_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_1, self.object8_1_not_equal2, self.object8_1_desc_alt))
        self.assertTrue(self.equality_tester.equal(self.object8_2, self.object8_2_equal, self.object8_2_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_2, self.object8_2_not_equal, self.object8_2_desc))
        self.assertTrue(self.equality_tester.equal(self.object8_2, self.object8_2_equal, self.object8_2_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_2, self.object8_2_not_equal, self.object8_2_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_2, self.object8_2_not_equal2, self.object8_2_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_2, self.object8_2_not_equal2, self.object8_2_desc_alt))
        self.assertTrue(self.equality_tester.equal(self.object8_3, self.object8_3_equal, self.object8_3_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_3, self.object8_3_not_equal, self.object8_3_desc))
        self.assertTrue(self.equality_tester.equal(self.object8_3, self.object8_3_equal, self.object8_3_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_3, self.object8_3_not_equal, self.object8_3_desc_alt))
        self.assertFalse(self.equality_tester.equal(self.object8_3, self.object8_3_not_equal2, self.object8_3_desc))
        self.assertFalse(self.equality_tester.equal(self.object8_3, self.object8_3_not_equal2, self.object8_3_desc_alt))
