from unittest import TestCase
import json
from datetime import datetime
        
from MAContainer_class import MAContainer
from MABooleanDescription_class import MABooleanDescription
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MAFloatDescription_class import MAFloatDescription
from MADateAndTimeDescription_class import MADateAndTimeDescription
from MASingleOptionDescription_class import MASingleOptionDescription

from MAVisitor_class import MAVisitor

class TestVisualizerVisitor(MAVisitor):
    
    def convert(self, model, description = None):
        if not description:
            if hasattr(model, "magritteDescription"):
                description = model.magritteDescription()

                self.json = None
                self.model = model
                
                self.visit(description)
                
                return self.json
            else:
                return model
        
    def deeper(self, model, description = None):
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
        value = description.accessor.read(self.model)
        
        try:
            json.dumps(value) #for test if value is json-serializable
            self.json[description.name] = value #if so, then just put raw value
        except:
            self.json[description.name] = f"!{value}!"

    def visitToOneRelationDescription(self, description):
        related_object = description.accessor.read(self.model)
        if(not description.reference):
            self.visitRelationDescription(description)
        else:
            self.json[description.name] = self.deeper(related_object)

    def visitToManyRelationDescription(self, description):
        collection = description.accessor.read(self.model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        self.json[description.name] = [self.deeper(entry) for entry in collection]

class MagritteSelfDescriptionTest(TestCase):

    def test_magritteDescription(self):

        object_desc = MAContainer()
        object_desc.label = "Demo Object"
        object_desc += MABooleanDescription(name='bool_value', label='Bool Value', default=True)
        object_desc += MAStringDescription(name='string_value', label='String Value', default='')
        object_desc += MAIntDescription(name='int_value', label='Int Value', default=0, min = 0)
        object_desc += MAFloatDescription(name='float_value', label='Float Value', default=0.0)
        object_desc += MADateAndTimeDescription(name='date_value', label='Date Value', default=datetime.now())
        object_desc += MASingleOptionDescription(name='color', label='Color Variants', options = ["red", "blue", "orange", "green"], default="orange", reference = MAStringDescription())

        child_obj_desc = MAContainer(label = "child object")
        child_obj_desc += MAStringDescription(name='string_value_of_child', label='String Value Of Child', default='')
        object_desc += MAToOneRelationDescription(name='child', label='Child object reference', reference = child_obj_desc)

        

        object_encoder = TestVisualizerVisitor()
        metadescriptor_json = object_encoder.convert(object_desc)
        
        print(f"description's description (in JSON):\n{json.dumps(metadescriptor_json, indent=4)}")
