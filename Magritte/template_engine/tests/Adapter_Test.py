from unittest import TestCase

import Cheetah.ErrorCatchers
import Cheetah.Template
from datetime import date

from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Port import Port
from Magritte.accessors.MAPluggableAccessor_class import MAPluggableAccessor
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.template_engine.MAModelCheetahTemplateAdapter_class import MAModelCheetahTemplateAdapter

class TestObject:
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
                

class MAAdapterTest(TestCase):

    def check_adapted_model(self, adapted_model):
        self.assertEqual(adapted_model['first'], "1")
        self.assertEqual(adapted_model['second'], "two")
        self.assertIsInstance(adapted_model['third'], str) #there are lot of ways to convert date to string, so we just test it's a string
        
        with self.assertRaises(Exception):
            adapted_model['nonexistent_field']
            
        print(f"From {adapted_model.model.__class__} => first: {adapted_model['first']}, second: {adapted_model['second']}, third: {adapted_model['third']}")
        
    def test_adaptation_from_tuple(self):
        model = (1, "two", date(2023, 3, 3))
        
        desc = MAContainer()
        desc += MAIntDescription(name="first", accessor=MAPluggableAccessor(lambda model: model[0], None))
        desc += MAStringDescription(name="second", accessor=MAPluggableAccessor(lambda model: model[1], None))
        desc += MADateDescription(name="third", accessor=MAPluggableAccessor(lambda model: model[2], None))
        
        adapted_model = MAModelCheetahTemplateAdapter(model, desc)
        self.check_adapted_model(adapted_model)

    def test_adaptation_from_object_with_attributes(self):
            
        model = TestObject(1, "two", date(2023, 3, 3))
        
        desc = MAContainer()
        desc += MAIntDescription(accessor="first")
        desc += MAStringDescription(accessor="second")
        desc += MADateDescription(accessor="third")
        
        adapted_model = MAModelCheetahTemplateAdapter(model, desc)
        self.check_adapted_model(adapted_model)
