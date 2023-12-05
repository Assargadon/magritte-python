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
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.template_engine.MAModelCheetahTemplateAdapter_class import MAModelCheetahTemplateAdapter
from Magritte.visitors.MAStringWriterReader_visitors import MAStringWriterVisitor

class TestObject:
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

class TestStringWriter(MAStringWriterVisitor):
                    
    def visitDateDescription(self, description: MADateDescription):
        datetime_str = description.accessor.read(self._model)
        self._val = datetime.strptime(datetime_str, '%d.%m.%Y').date()

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
        
    def test_different_stringifications(self):
        model = date(2023, 3, 3)
        
        desc = MAContainer()
        desc += MADateDescription(name="standard", accessor=MAIdentityAccessor())
        desc += MADateDescription(name="custom", accessor=MAIdentityAccessor(), stringWriter=TestStringWriter())

        adapted_model = MAModelCheetahTemplateAdapter(model, desc)
        print(f"standard: {adapted_model['standard']}, custom: {adapted_model['custom']}")
        
        
    def test_to_one_reference(self):

        inner_inner_model = (3, "three")
        inner_model = (2, "two", inner_inner_model)
        model = (1, "one", inner_model)
        
        inner_inner_desc = MAContainer()
        inner_inner_desc += MAIntDescription(name="num_field", accessor=MAPluggableAccessor(lambda model: model[0], None))
        inner_inner_desc += MAStringDescription(name="str_field", accessor=MAPluggableAccessor(lambda model: model[1], None))

        inner_desc = MAContainer()
        inner_desc += MAIntDescription(name="num_field", accessor=MAPluggableAccessor(lambda model: model[0], None))
        inner_desc += MAStringDescription(name="str_field", accessor=MAPluggableAccessor(lambda model: model[1], None))
        inner_desc += MAToOneRelationDescription(name="obj_field", accessor=MAPluggableAccessor(lambda model: model[2], None), reference=inner_inner_desc)
        
        desc = MAContainer()
        desc += MAIntDescription(name="num_field", accessor=MAPluggableAccessor(lambda model: model[0], None))
        desc += MAStringDescription(name="str_field", accessor=MAPluggableAccessor(lambda model: model[1], None))
        desc += MAToOneRelationDescription(name="obj_field", accessor=MAPluggableAccessor(lambda model: model[2], None), reference=inner_desc)

        adapted_model = MAModelCheetahTemplateAdapter(model, desc)
        self.assertEqual(adapted_model['num_field'], "1")
        self.assertEqual(adapted_model['obj_field']['num_field'], "2")
        self.assertEqual(adapted_model['obj_field']['obj_field']['num_field'], "3")
        # print(f"root level: {adapted_model['num_field']}, 2nd level: {adapted_model['obj_field']['num_field']}, 3rd level: {adapted_model['obj_field']['obj_field']['num_field']}")
        

    def test_to_many_scalar(self):
        model = ("object with array field", [1, 1, 2, 3, 5, 8, 13, 21])
 
        desc = MAContainer()
        desc += MAIntDescription(name="title", accessor=MAPluggableAccessor(lambda model: model[0], None))
        desc += MAToManyRelationDescription(name="fibbo", accessor=MAPluggableAccessor(lambda model: model[1], None), reference = MAIntDescription(accessor=MAIdentityAccessor()))

        adapted_model = MAModelCheetahTemplateAdapter(model, desc)
        
        self.assertEqual(len(adapted_model['fibbo']), len(model[1]))       

        for adapted, original in zip(adapted_model['fibbo'], model[1]):
            self.assertIsInstance(adapted, str)
            self.assertEqual(adapted, str(original))
          