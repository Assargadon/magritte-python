from unittest import TestCase
import json
from datetime import datetime

from descriptions.tests.AbstractTestForAllDescriptions import AbstractTestForAllDescriptions
from descriptions.MAContainer_class import MAContainer
from descriptions.MAPriorityContainer_class import MAPriorityContainer
from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MAFloatDescription_class import MAFloatDescription
from descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription

from visitors.MAVisitor_class import MAVisitor

class TestVisualizerVisitor(MAVisitor):
    
    def convert(self, model, description = None): #returns JSON representation of `model`
        if not description:
            try:
                description = model.magritteDescription()
            except (AttributeError, TypeError):
                return f"?{model}?"
    
        self.json = None
        self.model = model
        self.visit(description)
        return self.json
                
        
    def deeper(self, model, description = None):
        if model is None: return None #to avoid same condition in every place needed to convert value 
        if isinstance(model, (int, float, str, bool)): return model
        
        prev_json = self.json
        prev_model = self.model
        
        res = self.convert(model, description)

        self.json = prev_json
        self.model = prev_model
        
        return res

    def visitContainer(self, description):
        if not self.json:
            self.json = {}
            self.visitAll(description)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self.json")

    def visitElementDescription(self, description):

        value = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)        
        
        try:
            json.dumps(value) #for test if value is json-serializable
            self.json[description.name] = value #if so, then just put raw value
        except:
            if isinstance(value, (set, list)):
                self.json[description.name] = [self.deeper(entry) for entry in value]
            else:
                self.json[description.name] = f"!{value}!"

    def visitReferenceDescription(self, description): # i.e. model expected to be complex object (or collection of objects, but it's catched by visitMultipleOptionDescription and visitToManyRelationDescription below)
        model = description.accessor.read(self.model)
        if model is None:
            self.json[description.name] = None
        else:
            self.json[description.name] = self.deeper(model)

    def visitMultipleOptionDescription(self, description): # Mind that MAMultipleOptionDescription is not implemented yet
        selectedOptions = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        if selectedOptions is None:
            self.json[description.name] = None
        else:
            self.json[description.name] = {self.deeper(entry) for entry in selectedOptions}
       
    def visitToManyRelationDescription(self, description):
        collection = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        if collection is None:
            self.json[description.name] = None
        else:
            self.json[description.name] = [self.deeper(entry) for entry in collection]

        
        

class MagritteSelfDescriptionVisualTest(TestCase):

        
    def test_magritteDescription(self):
        object_desc = MAContainer()
        object_desc.label = "Demo Object"
        object_desc += MABooleanDescription(name='bool_value', label='Bool Value', default=True)
        object_desc += MAStringDescription(name='string_value', label='String Value', default='')
        object_desc += MAIntDescription(name='int_value', label='Int Value', default=0, min = 0)
        object_desc += MAFloatDescription(name='float_value', label='Float Value', default=0.0)
        object_desc += MADateAndTimeDescription(name='date_value', label='Date Value', default=datetime.now())
        object_desc += MASingleOptionDescription(name='color', label='Color Variants', options = ["red", "blue", "orange", "green"], default="orange", reference = MAStringDescription())


        class TestChild1:
            pass

        class TestChild2:
            pass

        child_obj_desc = MAContainer(label = "child object")
        child_obj_desc += MAStringDescription(name='string_value_of_child', label='String Value Of Child', default='')
        object_desc += MAToOneRelationDescription(name='child', label='Child object reference', reference = child_obj_desc, classes = {TestChild1, TestChild2})


        
        class EntryType1:
            pass

        class EntryType2:
            pass

        entry_desc = MAPriorityContainer(label = "entry object")
        entry_desc += MAStringDescription(name='comment', label='Comment', priority=20)
        entry_desc += MADateAndTimeDescription(name='timestamp', label='Entry Date', priority=10)
        object_desc += MAToManyRelationDescription(name='entries', label='Entries (child objects list)', reference = entry_desc, classes = {EntryType1, EntryType2})
        

        object_encoder = TestVisualizerVisitor()
        metadescriptor_json = object_encoder.convert(object_desc)
        
        print(f"description's description (in JSON):\n{json.dumps(metadescriptor_json, indent=4)}")
        
class MagritteSelfDescriptionTest(AbstractTestForAllDescriptions):

    def test_allDescriptorsHaveDescriptions(self):
        for desc in self.descriptors_to_test:
            with self.subTest(desc):
                metadescription = desc().magritteDescription()
                self.assertIsInstance(metadescription, MAContainer)
                self.assertTrue(len(metadescription) > 1)

    def test_allDescriptorsFieldsAreReadable(self):
        for desc in self.descriptors_to_test:
            with self.subTest(desc):
                description = desc()
                metadescription = description.magritteDescription()
                for desc_field_desc in metadescription:
                    val = description.readUsing(desc_field_desc)
                    #print(f"{desc.__name__}.{desc_field_desc.name} = `{val}`")
                    if(desc_field_desc.isRequired()):
                        #print(f"Mandatored {desc.__name__}.{desc_field_desc.name} = `{val}`")
                        self.assertIsNotNone(val, f"Field '{desc_field_desc.name}' of description {desc.__name__} is mandatored, but None")
                        
