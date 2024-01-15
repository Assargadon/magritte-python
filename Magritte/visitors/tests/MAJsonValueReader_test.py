from unittest import TestCase
import json
from datetime import datetime
from datetime import date


from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription

from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription


from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.visitors.MAJsonWriter_visitors import MAValueJsonReader


class ValueHolder:
    def __init__(self):
        self.value = None

class MAJsonReader_Test(TestCase):
    
    def setUp(self):
        self.holder = ValueHolder()
        self.json_reader = MAValueJsonReader()
    
    # "simple" conversion - i.e. jsonable type is the same as actual one

    def test_Int_decoding(self):
        desc = MAIntDescription(accessor = "value")
        actual_value = 13666
        json_value = 13666
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)

    def test_Float_decoding(self):
        desc = MAFloatDescription(accessor = "value")
        actual_value = 0.13666
        json_value = 0.13666
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)

    def test_String_decoding(self):
        desc = MAStringDescription(accessor = "value")
        actual_value = 13666
        json_value = 13666
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)

    def test_bool_decoding(self):
        desc = MABooleanDescription(accessor = "value")
        actual_value = False
        json_value = False
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)



    # "custom" conversion - i.e. actual type should be converted to jsonable one

    def test_DateAndTime(self):
        desc = MADateAndTimeDescription(accessor = "value")
        actual_value = datetime.now()
        json_value = actual_value.isoformat()
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)

    def test_Date(self):
        desc = MADateDescription(accessor = "value")
        actual_value = date.today()
        json_value = actual_value.isoformat()
        
        self.json_reader.read_json(self.holder, json_value, desc)
        self.assertEqual(self.holder.value, actual_value)
