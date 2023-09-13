# ==================== For testing. ====================
from datetime import datetime
from unittest import TestCase

from MAAttrAccessor_class import MAAttrAccessor
from MAContainer_class import MAContainer
from MADateAndTimeDescription_class import MADateAndTimeDescription
from MAFloatDescription_class import MAFloatDescription
from MAIdentityAccessor_class import MAIdentityAccessor
from MAIntDescription_class import MAIntDescription
from MARelationDescription_class import MARelationDescription
from MAStringDescription_class import MAStringDescription
from MAJsonWriter_visitors import MAValueJsonWriter, MAObjectJsonWriter


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


class MAJsonWriter_Test(TestCase):
    def setUp(self):
        # ==================== Scalar values testing. ====================
        self.int_value = 123
        self.int_desc = MAIntDescription(name='TestInt', label='Test Int', default=0, accessor=MAIdentityAccessor())
        self.int_encoder = MAValueJsonWriter(self.int_desc)

        self.str_value = 'abc'
        self.str_desc = MAStringDescription(name='TestString', label='Test String', default='',
                                       accessor=MAIdentityAccessor())
        self.str_encoder = MAValueJsonWriter(self.str_desc)

        self.float_value = 1.23
        self.float_desc = MAFloatDescription(name='TestFloat', label='Test Float', default=0.0,
                                        accessor=MAIdentityAccessor())
        self.float_encoder = MAValueJsonWriter(self.float_desc)

        self.date_value = datetime.now()
        self.date_desc = MADateAndTimeDescription(
            name='TestDate', label='Test Date', default=datetime.now(), accessor=MAIdentityAccessor()
        )
        self.date_encoder = MAValueJsonWriter(self.date_desc)

        self.scalar_rel_value = self.int_value
        self.scalar_rel_desc = MARelationDescription(
            name='TestScalarRel', label='Test Scalar Relation', accessor=MAIdentityAccessor()
        )
        # Cannot set reference in constructor because of current MARelationDescription implementation.
        self.scalar_rel_desc.reference = self.int_desc
        self.scalar_rel_encoder = MAValueJsonWriter(self.scalar_rel_desc)

        # ==================== Object encoding testing. ====================
        self.object1 = TestObject1('object1', 123, 1.23, datetime.now())
        self.object_desc = MAContainer()
        self.object_desc.setChildren(
            [
                MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
                MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
                MAFloatDescription(
                    name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
                ),
                MADateAndTimeDescription(
                    name='date_value', label='Date Value', default=datetime.now(),
                    accessor=MAAttrAccessor('date_value'),
                ),
            ]
        )
        self.object_encoder = MAObjectJsonWriter(self.object_desc)

        # ==================== Object reference value testing. ====================
        self.object_rel_desc = MARelationDescription(
            name='TestObjectRel', label='Test Object Relation', accessor=MAIdentityAccessor()
        )
        # Cannot set reference in constructor because of current MARelationDescription implementation.
        self.object_rel_desc.reference = self.object_desc
        self.object_rel_encoder = MAValueJsonWriter(self.object_rel_desc)

        # ==================== Compound object with reference testing. ====================
        self.compound_object = TestObject2('object2', 234, 2.34, datetime.now(), self.object1)
        self.compound_object_desc = MAContainer()
        self.compound_object_desc.setChildren([
            MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
            MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
            MAFloatDescription(
                name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
            ),
            MADateAndTimeDescription(
                name='date_value', label='Date Value', default=datetime.now(), accessor=MAAttrAccessor('date_value'),
            ),
            MARelationDescription(name='ref_object', label='Referenced Object', accessor=MAAttrAccessor('ref_object')),
        ])
        # Cannot set reference in constructor because of current MARelationDescription implementation.
        self.compound_object_desc.children[4].reference = self.object_desc
        self.compound_object_encoder = MAObjectJsonWriter(self.compound_object_desc)

    def test_int_encoder(self):
        self.assertEqual(self.int_encoder.write_json(self.int_value), 123)
        self.assertEqual(self.int_encoder.write_json_string(self.int_value), '123')

    def test_str_encoder(self):
        self.assertEqual(self.str_encoder.write_json(self.str_value), 'abc')
        self.assertEqual(self.str_encoder.write_json_string(self.str_value), '"abc"')

    def test_float_encoder(self):
        self.assertEqual(self.float_encoder.write_json(self.float_value), 1.23)
        self.assertEqual(self.float_encoder.write_json_string(self.float_value), '1.23')

    def test_date_encoder(self):
        self.assertEqual(self.date_encoder.write_json(self.date_value), datetime.now().isoformat())
        self.assertEqual(self.date_encoder.write_json_string(self.date_value), f'"{datetime.now().isoformat()}"')

    def test_scalar_encoder(self):
        self.assertEqual(self.scalar_rel_encoder.write_json(self.scalar_rel_value), self.int_value)
        self.assertEqual(self.scalar_rel_encoder.write_json_string(self.scalar_rel_value), str(self.int_value))

    def test_object_encoder(self):
        self.assertEqual(self.object_encoder.write_json(self.object1),
                         {'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': datetime.now().isoformat()})
        # self.assertEqual(self.object_encoder.write_json_string(self.object1),
        #                  {"name": "object1", "int_value": 123, "float_value": 1.23, "date_value": f"{datetime.now().isoformat()}"})

    def test_object_rel_encoder(self):
        self.assertEqual(self.object_rel_encoder.write_json(self.object1),
                         {'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': datetime.now().isoformat()})
        # self.assertEqual(self.object_rel_encoder.write_json_string(self.object1),
        #                  {"name": "object1", "int_value": 123, "float_value": 1.23, "date_value": f"{datetime.now().isoformat()}"})

    def test_compound_object_encoder(self):
        self.assertEqual(self.compound_object_encoder.write_json(self.compound_object),
                         {'name': 'object2', 'int_value': 234, 'float_value': 2.34, 'date_value': datetime.now().isoformat(),
                          'ref_object': {'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': datetime.now().isoformat()}})
        # self.assertEqual(self.compound_object_encoder.write_json(self.compound_object),
        #                  {"name": "object2", "int_value": 234, "float_value": 2.34, "date_value": f'"{datetime.now().isoformat()}"',
        #                   "ref_object": {"name": "object1", "int_value": 123, "float_value": 1.23, "date_value": f'"{datetime.now().isoformat()}"'}})


# if __name__ == "__main__":
#
#     # ==================== Scalar values testing. ====================
#     print(" ==================== Scalar values testing. ====================")
#     int_value = 123
#     int_desc = MAIntDescription(name='TestInt', label='Test Int', default=0, accessor=MAIdentityAccessor())
#     int_encoder = MAValueJsonWriter(int_desc)
#     print(f"jsonable value for int_value: {int_encoder.write_json(int_value)}.")
#     print(f"json string for int_value: {int_encoder.write_json_string(int_value)}.")
#
#     str_value = 'abc'
#     str_desc = MAStringDescription(name='TestString', label='Test String', default='', accessor=MAIdentityAccessor())
#     str_encoder = MAValueJsonWriter(str_desc)
#     print(f"jsonable value for str_value: {str_encoder.write_json(str_value)}.")
#     print(f"json string for str_value: {str_encoder.write_json_string(str_value)}.")
#
#     float_value = 1.23
#     float_desc = MAFloatDescription(name='TestFloat', label='Test Float', default=0.0, accessor=MAIdentityAccessor())
#     float_encoder = MAValueJsonWriter(float_desc)
#     print(f"jsonable value for float_value: {float_encoder.write_json(float_value)}.")
#     print(f"json string for float_value: {float_encoder.write_json_string(float_value)}.")
#
#     date_value = datetime.now()
#     date_desc = MADateAndTimeDescription(
#         name='TestDate', label='Test Date', default=datetime.now(), accessor=MAIdentityAccessor()
#         )
#     date_encoder = MAValueJsonWriter(date_desc)
#     print(f"jsonable value for date_value: {date_encoder.write_json(date_value)}.")
#     print(f"json string for date_value: {date_encoder.write_json_string(date_value)}.")
#
#     scalar_rel_value = int_value
#     scalar_rel_desc = MARelationDescription(
#         name='TestScalarRel', label='Test Scalar Relation', accessor=MAIdentityAccessor()
#         )
#     # Cannot set reference in constructor because of current MARelationDescription implementation.
#     scalar_rel_desc.reference = int_desc
#     scalar_rel_encoder = MAValueJsonWriter(scalar_rel_desc)
#     print(f"jsonable value for scalar_rel_value: {scalar_rel_encoder.write_json(scalar_rel_value)}.")
#     print(f"json string for scalar_rel_value: {scalar_rel_encoder.write_json_string(scalar_rel_value)}.")
#
#     # ==================== Object encoding testing. ====================
#     print(" ==================== Object encoding testing. ====================")
#     object1 = TestObject1('object1', 123, 1.23, datetime.now())
#     object_desc = MAContainer()
#     object_desc.setChildren(
#         [
#             MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
#             MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
#             MAFloatDescription(
#                 name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
#                 ),
#             MADateAndTimeDescription(
#                 name='date_value', label='Date Value', default=datetime.now(), accessor=MAAttrAccessor('date_value'),
#                 ),
#             ]
#         )
#     object_encoder = MAObjectJsonWriter(object_desc)
#     print(f"jsonable value for object1: {object_encoder.write_json(object1)}.")
#     print(f"json string for object1: {object_encoder.write_json_string(object1)}.")
#
#     # ==================== Object reference value testing. ====================
#     print(" ==================== Object reference value testing. ====================")
#     object_rel_desc = MARelationDescription(
#         name='TestObjectRel', label='Test Object Relation', accessor=MAIdentityAccessor()
#         )
#     # Cannot set reference in constructor because of current MARelationDescription implementation.
#     object_rel_desc.reference = object_desc
#     object_rel_encoder = MAValueJsonWriter(object_rel_desc)
#     print(f"jsonable value for reference->object1: {object_rel_encoder.write_json(object1)}.")
#     print(f"json string for reference->object1: {object_rel_encoder.write_json_string(object1)}.")
#
#     # ==================== Compound object with reference testing. ====================
#     print(" ==================== Compound object with reference testing. ====================")
#     compound_object = TestObject2('object2', 234, 2.34, datetime.now(), object1)
#     compound_object_desc = MAContainer()
#     compound_object_desc.setChildren([
#         MAStringDescription(name='name', label='Name', default='', accessor=MAAttrAccessor('name')),
#         MAIntDescription(name='int_value', label='Int Value', default=0, accessor=MAAttrAccessor('int_value')),
#         MAFloatDescription(
#             name='float_value', label='Float Value', default=0.0, accessor=MAAttrAccessor('float_value'),
#             ),
#         MADateAndTimeDescription(
#             name='date_value', label='Date Value', default=datetime.now(), accessor=MAAttrAccessor('date_value'),
#             ),
#         MARelationDescription(name='ref_object', label='Referenced Object', accessor=MAAttrAccessor('ref_object')),
#         ])
#     # Cannot set reference in constructor because of current MARelationDescription implementation.
#     compound_object_desc.children[4].reference = object_desc
#     compound_object_encoder = MAObjectJsonWriter(compound_object_desc)
#     print(f"jsonable value for compound_object: {compound_object_encoder.write_json(compound_object)}.")
#     print(f"json string for compound_object: {compound_object_encoder.write_json_string(compound_object)}.")
