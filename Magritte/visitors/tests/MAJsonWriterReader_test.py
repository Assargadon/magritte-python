# ==================== For testing. ====================
from datetime import datetime, time, date
from typing import List
from unittest import TestCase
import json
import sys

from Magritte.descriptions.MAOptionDescription_class import MAOptionDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription

from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor

from Magritte.visitors.MAJsonWriterReader_visitors import MAObjectJsonReader, MAValueJsonReader, MAValueJsonWriter, MAObjectJsonWriter

#sys.stdout = open('output.txt', 'w')

class Testobject1:
    def __init__(
            self, name: str, int_val: int, 
            float_val: float, date_val: datetime
        ):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val


class Testobject2:
    def __init__(
            self, name: str, int_val: int, float_val: float, 
            date_val: datetime, ref_object: Testobject1
        ):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_object = ref_object


class Testobject3:
    def __init__(
            self, name: str, int_val: int, float_val: float, 
            date_val: datetime, ref_objects: List[Testobject1]
        ):
        self.name = name
        self.int_value = int_val
        self.date_value = date_val
        self.float_value = float_val
        self.ref_objects = ref_objects


class TestGlossary:
    def __init__(self, name: str):
        self.name = name


class Testobject4:
    def __init__(self, name: str, selection: TestGlossary):
        self.name = name
        self.selection = selection


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
        self.object_1 = Testobject1('object_1', 123, 1.23, self.time_now)
        self.object_2 = Testobject1('object_2', 234, 2.34, self.time_now)
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
        self.compound_object = Testobject2('object_3', 345, 3.45, self.time_now, self.object_1)
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
        self.compound_object_2 = Testobject3(
            'object_4', 456, 4.56, self.time_now, [self.object_1, self.object_2]
            )
        self.compound_object_2_desc = MAContainer()
        self.compound_object_2_desc.setChildren(
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

        self.object_4 = Testobject4('object_4', self.glossary1)
        self.object_4_desc = MAContainer()
        self.object_4_desc.setChildren(
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
            self.value_encoder.write_json(self.object_1, self.object_desc)
        with self.assertRaises(TypeError):
            self.value_encoder.write_json_string(self.object_1, self.object_desc)

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
            self.object_encoder.write_json(self.object_1, self.object_desc),
            {'name': 'object_1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()}
            )
        json_string = self.object_encoder.write_json_string(self.object_1, self.object_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {"name": "object_1", "int_value": 123, "float_value": 1.23, "date_value": f"{self.time_now.isoformat()}"}
            )

    '''
    # Think whether we need this test.
    def test_object_rel_encoder(self):
        self.assertEqual(
            self.object_rel_encoder.write_json(self.object_1),
            {'name': 'object_1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()})
        json_string = self.object_rel_encoder.write_json_string(self.object_1)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {"name": "object_1", "int_value": 123, "float_value": 1.23, "date_value": f"{self.time_now.isoformat()}"}
            )
    '''

    def test_compound_object_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.compound_object, self.compound_object_desc),
            {
                'name': 'object_3', 'int_value': 345, 'float_value': 3.45, 'date_value': self.time_now.isoformat(),
                'ref_object': {
                    'name': 'object_1', 'int_value': 123, 'float_value': 1.23, 'date_value': self.time_now.isoformat()
                    }
                }
            )
        json_string = self.object_encoder.write_json_string(self.compound_object, self.compound_object_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object_3", "int_value": 345, "float_value": 3.45, "date_value": f"{self.time_now.isoformat()}",
                "ref_object": {
                    "name": "object_1", "int_value": 123, "float_value": 1.23,
                    "date_value": f"{self.time_now.isoformat()}"
                    }
                }
            )

    def test_compound_object_2_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.compound_object_2, self.compound_object_2_desc),
            {
                'name': 'object_4', 'int_value': 456, 'float_value': 4.56, 'date_value': self.time_now.isoformat(),
                'ref_objects': [
                    {
                        'name': 'object_1', 'int_value': 123, 'float_value': 1.23,
                        'date_value': self.time_now.isoformat()
                        },
                    {
                        'name': 'object_2', 'int_value': 234, 'float_value': 2.34,
                        'date_value': self.time_now.isoformat()
                        }
                    ]
                }
            )
        json_string = self.object_encoder.write_json_string(self.compound_object_2, self.compound_object_2_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object_4", "int_value": 456, "float_value": 4.56, "date_value": f"{self.time_now.isoformat()}",
                "ref_objects": [
                    {
                        "name": "object_1", "int_value": 123, "float_value": 1.23,
                        "date_value": f"{self.time_now.isoformat()}"
                        },
                    {
                        "name": "object_2", "int_value": 234, "float_value": 2.34,
                        "date_value": f"{self.time_now.isoformat()}"
                        }
                    ]
                }
            )

    def test_object_with_option_encoder(self):
        self.assertEqual(
            self.object_encoder.write_json(self.object_4, self.object_4_desc),
            {
                'name': 'object_4', 'selection': {'name': 'glossary1'}
                }
            )
        json_string = self.object_encoder.write_json_string(self.object_4, self.object_4_desc)
        obj = json.loads(json_string)
        self.assertEqual(
            obj,
            {
                "name": "object_4", "selection": {"name": "glossary1"}
                }
            )


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
        self.object_1 = Testobject1('object_1', 123, 1.23, self.time_now)
        self.object_2 = Testobject1('object_2', 234, 2.34, self.time_now)

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


class ResponseObject:
    pass


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
        self.object_1 = ResponseObject()
        self.object_1.name = 'object_1'
        self.object_1.int_value = 123
        self.object_1.float_value = 1.23
        self.object_1.date_value = self.time_now

        self.object_2 = ResponseObject()
        self.object_2.name = 'object_2'
        self.object_2.int_value = 234
        self.object_2.float_value = 2.34
        self.object_2.date_value = self.time_now



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

        self.compound_json = json.dumps(
            {
                'name': 'object_3', 
                'int_value': 345, 
                'float_value': 3.45, 
                'date_value': str(self.time_now),
                'ref_object': {
                    'name': 'object_1',
                    'int_value': 123,
                    'float_value': 1.23,
                    'date_value': str(self.time_now)
                }
            }
        )

        self.compound_json_2 = json.dumps(
            {
                "name": "object_3", 
                "int_value": 345, 
                "float_value": 3.45, 
                "date_value": str(self.time_now),
                "ref_object": {
                    "name": "object_1", 
                    "int_value": 123, 
                    "float_value": 1.23,
                    "date_value": str(self.time_now)
                }
            }
        )

        self.ref_object = ResponseObject()
        self.ref_object.name = 'object_1'
        self.ref_object.int_value = 123
        self.ref_object.float_value = 1.23
        self.ref_object.date_value = self.time_now

        self.compound_object = ResponseObject()
        self.compound_object.name = 'object_3'
        self.compound_object.int_value = 345
        self.compound_object.float_value = 3.45
        self.compound_object.date_value = self.time_now
        self.compound_object.ref_object=self.ref_object


        self.compound_object_desc = MAContainer()
        self.compound_object_desc.setChildren(
            [
                MAStringDescription(label='Name', default='', accessor='name'),
                MAIntDescription(label='Int Value', default=0, accessor='int_value'),
                MAFloatDescription(
                    label='Float Value', default=0.0, accessor='float_value'
                ),
                MADateAndTimeDescription(
                    label='Date Value', default=self.time_now, accessor='date_value'
                ),
                MAToOneRelationDescription(
                    label='Referenced Object', accessor='ref_object', reference=self.object_desc
                ),]
            )

        # ==================== Compound object with to-many relation testing. ====================
        self.mtm_compound_object = ResponseObject()
        self.mtm_compound_object.name = 'object_4'
        self.mtm_compound_object.int_value = 456
        self.mtm_compound_object.float_value = 4.56
        self.mtm_compound_object.date_value = self.time_now
        self.mtm_compound_object.ref_objects=[self.object_1, self.object_2]

        self.mtm_compound_object_desc = MAContainer()
        self.mtm_compound_object_desc.setChildren(
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

        self.mtm_json_1 = json.dumps(
            {
                'name': 'object_4', 'int_value': 456, 'float_value': 4.56, 'date_value': str(self.time_now),
                'ref_objects': [
                    {
                        'name': 'object_1', 'int_value': 123, 'float_value': 1.23,
                        'date_value': str(self.time_now)
                        },
                    {
                        'name': 'object_2', 'int_value': 234, 'float_value': 2.34,
                        'date_value': str(self.time_now)
                        }
                    ]
                }
        )


    def test_object_decoding(self):
        obj = self.object_decoder.read_json(self.json_1, self.object_desc)
        
        obj_dict = {k: v for k, v in obj.__dict__.items() if k != 'self'}
        comp_obj_dict = {k: v for k, v in self.object_1.__dict__.items() if k != 'self'}
        self.assertEqual(obj_dict, comp_obj_dict, f"Object mismatch: {obj_dict} != {comp_obj_dict}")

        obj = self.object_decoder.read_json(self.json_2, self.object_desc)

        obj_dict = {k: v for k, v in obj.__dict__.items() if k != 'self'}
        comp_obj_dict = {k: v for k, v in self.object_2.__dict__.items() if k != 'self'}

        self.assertEqual(obj_dict, comp_obj_dict, f"Object mismatch: {obj_dict} != {comp_obj_dict}")


    def test_compound_object_decoder(self):
        obj = self.object_decoder.read_json(self.compound_json, self.compound_object_desc)

        self.assertEqual(obj.name, self.compound_object.name)
        self.assertEqual(obj.int_value, self.compound_object.int_value)
        self.assertEqual(obj.float_value, self.compound_object.float_value)
        self.assertEqual(obj.date_value, self.compound_object.date_value)

        obj_dict = {k: v for k, v in obj.ref_object.__dict__.items() if k != 'self'}
        comp_obj_dict = {k: v for k, v in self.compound_object.ref_object.__dict__.items() if k != 'self'}

        self.assertEqual(obj_dict, comp_obj_dict, f"Object mismatch: {obj_dict} != {comp_obj_dict}")


    def test_many_to_many_decoder(self):
        obj = self.object_decoder.read_json(self.mtm_json_1, self.mtm_compound_object_desc)

        self.assertEqual(obj.name, self.mtm_compound_object.name)
        self.assertEqual(obj.int_value, self.mtm_compound_object.int_value)
        self.assertEqual(obj.float_value, self.mtm_compound_object.float_value)
        self.assertEqual(obj.date_value, self.mtm_compound_object.date_value)

        for i in range(len(self.mtm_compound_object.ref_objects)):
            obj_dict = {k: v for k, v in obj.ref_objects[i].__dict__.items() if k != 'self'}
            comp_obj_dict = {k: v for k, v in self.mtm_compound_object.ref_objects[i].__dict__.items() if k != 'self'}

            self.assertEqual(obj_dict, comp_obj_dict, f"Object mismatch: {obj_dict} != {comp_obj_dict}")