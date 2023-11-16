# ==================== For testing. ====================
from datetime import datetime
from typing import List
from unittest import TestCase
import json

from Magritte.descriptions.MAOptionDescription_class import MAOptionDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription

from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor

from Magritte.visitors.MAJsonWriter_visitors import MAObjectJsonReader, MAValueJsonReader, MAValueJsonWriter, MAObjectJsonWriter


class TestObject1:
    def __init__(self, name: str, int_val: int, float_val: float, date_val: datetime):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class TestObject2:
    def __init__(self, name: str, int_val: int, float_val: float, 
                 date_val: datetime, ref_object: TestObject1
        ):
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

"""
class MAJsonWriter_Test(TestCase):
    def setUp(self):
        # ==================== Encoders for testing. ====================
        self.value_encoder = MAValueJsonWriter()
        self.object_encoder = MAObjectJsonWriter()

        # ==================== Scalar values testing. ====================
        self.int_value = 123
        self.int_desc = MAIntDescription(name='TestInt', label='Test Int', default=0, accessor=MAIdentityAccessor())

        self.str_value = 'abc'
        self.str_desc = MAStringDescription(
            name='TestString', label='Test String', default='',
            accessor=MAIdentityAccessor()
            )
        self.float_value = 1.23
        self.float_desc = MAFloatDescription(
            name='TestFloat', label='Test Float', default=0.0,
            accessor=MAIdentityAccessor()
            )

        self.time_now = datetime.now()
        self.date_value = self.time_now
        self.date_desc = MADateAndTimeDescription(
            name='TestDate', label='Test Date', default=self.time_now, accessor=MAIdentityAccessor()
            )

        # ==================== Scalar relation value testing. ====================
        self.scalar_rel_value = self.int_value
        self.scalar_rel_desc = MAToOneRelationDescription(
            name='TestScalarRel', label='Test Scalar Relation', accessor=MAIdentityAccessor(), reference=self.int_desc
            )

        # ==================== Object encoding testing. ====================
        self.object1 = TestObject1('object1', 123, 1.23, self.time_now)
        self.object2 = TestObject1('object2', 234, 2.34, self.time_now)
        self.object_desc = MAContainer()
        self.object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
                ]
            )

        '''
        # ==================== Object reference value testing. ====================
        self.object_rel_desc = MAToOneRelationDescription(
            name='TestObjectRel', label='Test Object Relation', accessor=MAIdentityAccessor()
            )
        # Cannot set reference in constructor because of current MARelationDescription implementation.
        self.object_rel_desc.reference = self.object_desc
        '''

        # ==================== Compound object with to-one relation testing. ====================
        self.compound_object = TestObject2('object3', 345, 3.45, self.time_now, self.object1)
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

        # ==================== Compound object with to-many relation testing. ====================
        self.compound_object2 = TestObject3(
            'object4', 456, 4.56, self.time_now, [self.object1, self.object2]
            )
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

        # ==================== Object with option testing. ====================
        self.glossary1 = TestGlossary('glossary1')
        self.glossary2 = TestGlossary('glossary2')
        self.glossary_desc = MAContainer()
        self.glossary_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                ]
            )

        self.object4 = TestObject4('object4', self.glossary1)
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

    def test_int_encoding(self):
        self.assertEqual(self.value_encoder.write_json(self.int_value, self.int_desc), 123)
        json_string = self.value_encoder.write_json_string(self.int_value, self.int_desc)
        obj = json.loads(json_string)
        self.assertEqual(obj, 123)

    def test_str_encoding(self):
        self.assertEqual(self.value_encoder.write_json(self.str_value, self.str_desc), 'abc')
        json_string = self.value_encoder.write_json_string(self.str_value, self.str_desc)
        obj = json.loads(json_string)
        self.assertEqual(obj, 'abc')

    def test_float_encoding(self):
        self.assertEqual(self.value_encoder.write_json(self.float_value, self.float_desc), 1.23)
        json_string = self.value_encoder.write_json_string(self.float_value, self.float_desc)
        obj = json.loads(json_string)
        self.assertEqual(obj, 1.23)

    def test_date_encoding(self):
        self.assertEqual(self.value_encoder.write_json(self.date_value, self.date_desc), self.time_now.isoformat())
        json_string = self.value_encoder.write_json_string(self.date_value, self.date_desc)
        obj = json.loads(json_string)
        self.assertEqual(obj, self.time_now.isoformat())

    def test_error_relation_description(self):
        with self.assertRaises(TypeError):
            self.value_encoder.write_json(self.scalar_rel_value, self.scalar_rel_desc)
        with self.assertRaises(TypeError):
            self.value_encoder.write_json_string(self.scalar_rel_value, self.scalar_rel_desc)

    def test_error_object_value(self):
        with self.assertRaises(TypeError):
            self.value_encoder.write_json(self.object1, self.object_desc)
        with self.assertRaises(TypeError):
            self.value_encoder.write_json_string(self.object1, self.object_desc)

    '''
    # Think whether we need this test.
    def test_scalar_rel_encoding(self):
        self.assertEqual(self.object_encoder.write_json(self.scalar_rel_value, self.scalar_rel_desc), self.int_value)
        json_string = self.object_encoder.write_json_string(self.scalar_rel_value, self.scalar_rel_desc)
        obj = json.loads(json_string)
        self.assertEqual(obj, self.int_value)
    '''

    def test_object_encoding(self):
        self.assertEqual(
            self.object_encoder.write_json(self.object1, self.object_desc),
            {'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()}
            )
        json_string = self.object_encoder.write_json_string(self.object1, self.object_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {"name": "object1", "int_value": 123, "float_value": 1.23, "date_value": f"{self.time_now.isoformat()}"}
            )

    '''
    # Think whether we need this test.
    def test_object_rel_encoder(self):
        self.assertEqual(
            self.object_rel_encoder.write_json(self.object1),
            {'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()})
        json_string = self.object_rel_encoder.write_json_string(self.object1)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {"name": "object1", "int_value": 123, "float_value": 1.23, "date_value": f"{self.time_now.isoformat()}"}
            )
    '''

    def test_compound_object_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.compound_object, self.compound_object_desc),
            {
                'name': 'object3', 'int_value': 345, 'float_value': 3.45, 'date_value': self.time_now.isoformat(),
                'ref_object': {
                    'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()
                    }
                }
            )
        json_string = self.object_encoder.write_json_string(self.compound_object, self.compound_object_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object3", "int_value": 345, "float_value": 3.45, "date_value": f"{self.time_now.isoformat()}",
                "ref_object": {
                    "name": "object1", "int_value": 123, "float_value": 1.23,
                    "date_value": f"{self.time_now.isoformat()}"
                    }
                }
            )

    def test_compound_object2_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.compound_object2, self.compound_object2_desc),
            {
                'name': 'object4', 'int_value': 456, 'float_value': 4.56, 'date_value': self.time_now.isoformat(),
                'ref_objects': [
                    {
                        'name': 'object1', 'int_value': 123, 'float_value': 1.23,
                        'date_value': self.time_now.isoformat()
                        },
                    {
                        'name': 'object2', 'int_value': 234, 'float_value': 2.34,
                        'date_value': self.time_now.isoformat()
                        }
                    ]
                }
            )
        json_string = self.object_encoder.write_json_string(self.compound_object2, self.compound_object2_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object4", "int_value": 456, "float_value": 4.56, "date_value": f"{self.time_now.isoformat()}",
                "ref_objects": [
                    {
                        "name": "object1", "int_value": 123, "float_value": 1.23,
                        "date_value": f"{self.time_now.isoformat()}"
                        },
                    {
                        "name": "object2", "int_value": 234, "float_value": 2.34,
                        "date_value": f"{self.time_now.isoformat()}"
                        }
                    ]
                }
            )

    def test_object_with_option_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.object4, self.object4_desc),
            {
                'name': 'object4', 'selection': {'name': 'glossary1'}
                }
            )
        json_string = self.object_encoder.write_json_string(self.object4, self.object4_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object4", "selection": {"name": "glossary1"}
                }
            )

"""
class MAJsonReader_Test(TestCase):
    def setUp(self):
        self.value_decoder = MAValueJsonReader()
        #self.object_decoder = MAObjectJsonReader()

    # ==================== Scalar values testing. ====================
        self.int_value = 123
        self.int_desc = MAIntDescription(
            name='TestInt', label='Test Int', default=0, 
            accessor=MAIdentityAccessor()
        )

        self.str_desc = MAStringDescription(
            name='TestString', label='Test String', default='',
            accessor=MAIdentityAccessor()
        )

        self.float_desc = MAFloatDescription(
            name='TestFloat', label='Test Float', default=0.0,
            accessor=MAIdentityAccessor()
        )

        self.time_now = datetime.now()
        self.date_desc = MADateAndTimeDescription(
            name='TestDate', label='Test Date', default=self.time_now, 
            accessor=MAIdentityAccessor()
        )

        # ==================== Object encoding testing. ====================
        self.object_1 = TestObject1('object1', 123, 1.23, self.time_now)
        self.object_2 = TestObject1('object2', 234, 2.34, self.time_now)

        self.json_1 = json.dumps(
            {
                "name": "object_1", 
                "int_value": 123, 
                "float_value": 1.23, 
                "date_value": str(self.time_now)
            }
        )
        self.json_2 = json.dumps(
            {
                "name": "object_2", 
                "int_value": 234, 
                "float_value": 2.34, 
                "date_value": str(self.time_now)
            }
        )

        self.object_desc = MAContainer()
        self.object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_value'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_value'),
            ]
        )

    def test_int_decoding(self):
        attr_value = self.value_decoder.read_json(json.loads(self.json_1)['int_value'], self.int_desc)
        self.assertEqual(attr_value, 123)

    def test_str_decoding(self):
        attr_value = self.value_decoder.read_json(json.loads(self.json_1)['name'], self.str_desc)
        self.assertEqual(attr_value, 'object_1')

    def test_float_decoding(self):
        attr_value = self.value_decoder.read_json(json.loads(self.json_1)['float_value'], self.float_desc)
        self.assertEqual(attr_value, 1.23)

    def test_date_decoding(self):
        attr_value = self.value_decoder.read_json(json.loads(self.json_1)['date_value'], self.date_desc)
        self.assertEqual(attr_value, self.time_now)

class MAJsonObjectReader_Test(TestCase):
    def setUp(self):
        self.object_decoder = MAObjectJsonReader()

    # ==================== Scalar values testing. ====================
        self.int_value = 123
        self.int_desc = MAIntDescription(
            name='TestInt', label='Test Int', default=0, 
            accessor=MAIdentityAccessor()
        )

        self.str_desc = MAStringDescription(
            name='TestString', label='Test String', default='',
            accessor=MAIdentityAccessor()
        )

        self.float_desc = MAFloatDescription(
            name='TestFloat', label='Test Float', default=0.0,
            accessor=MAIdentityAccessor()
        )

        self.time_now = datetime.now()
        self.date_desc = MADateAndTimeDescription(
            name='TestDate', label='Test Date', default=self.time_now, 
            accessor=MAIdentityAccessor()
        )

        # ==================== Object encoding testing. ====================
        self.object_1 = TestObject1('object1', 123, 1.23, self.time_now)
        self.object_2 = TestObject1('object2', 234, 2.34, self.time_now)

        self.json_1 = json.dumps(
            {
                "name": "object_1", 
                "int_val": 123, 
                "float_val": 1.23, 
                "date_val": str(self.time_now)
            }
        )
        self.json_2 = json.dumps(
            {
                "name": "object_2", 
                "int_val": 234, 
                "float_val": 2.34, 
                "date_val": str(self.time_now)
            }
        )

        self.object_desc = MAContainer()
        self.object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_val'),
                MAFloatDescription(label='Float Value', default=0.0, accessor='float_val'),
                MADateAndTimeDescription(label='Date Value', default=self.time_now, accessor='date_val'),
            ]
        )

    def test_object_decoding(self):
        obj = self.object_decoder.read_json(self.json_1, self.object_desc),
        self.assertEqual(obj, self.object_1)

        obj = self.object_decoder.read_json(self.json_2, self.object_desc)
        self.assertEqual(obj, self.object_2)

    '''
    def test_compound_object_encoder(self):
        self.assertEqual(
            self.object_decoder.read_json(self.compound_object, self.compound_object_desc),
            {
                'name': 'object3', 'int_value': 345, 'float_value': 3.45, 'date_value': self.time_now.isoformat(),
                'ref_object': {
                    'name': 'object1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()
                    }
                }
            )
        json_string = self.object_encoder.write_json_string(self.compound_object, self.compound_object_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object3", "int_value": 345, "float_value": 3.45, "date_value": f"{self.time_now.isoformat()}",
                "ref_object": {
                    "name": "object1", "int_value": 123, "float_value": 1.23,
                    "date_value": f"{self.time_now.isoformat()}"
                    }
                }
            )
        '''