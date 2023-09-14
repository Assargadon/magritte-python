from unittest import TestCase
import json

from MAContainer_class import MAContainer
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MAFloatDescription_class import MAFloatDescription
from MADateAndTimeDescription_class import MADateAndTimeDescription


class MagritteSelfDescriptionTest(TestCase):

    def test_magritteDescription(self):
        from datetime import datetime
        from MAJsonWriter_visitors import MAValueJsonWriter, MAObjectJsonWriter

        object_desc = MAContainer()
        object_desc.label = "Demo Object"
        object_desc += MAStringDescription(name='string_value', label='String Value', default='')
        object_desc += MAIntDescription(name='int_value', label='Int Value', default=0)
        object_desc += MAFloatDescription(name='float_value', label='Float Value', default=0.0)
        object_desc += MADateAndTimeDescription(name='date_value', label='Date Value', default=datetime.now())

        object_encoder = MAObjectJsonWriter(object_desc.magritteDescription())
        metadescriptor_json = object_encoder.write_json(object_desc)
        
        print(f"description's description (in JSON):\n{json.dumps(metadescriptor_json, indent=4)}")
