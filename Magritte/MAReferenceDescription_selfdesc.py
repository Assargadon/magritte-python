from accessors.MAAttrAccessor_class import MAAttrAccessor
from MAToOneRelationDescription_class import MAToOneRelationDescription
from MADescription_class import MADescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MAToOneRelationDescription(label = "Description", priority = 400, classes = [MADescription], accessor = MAAttrAccessor('reference'), comment = "Description of the dependent model used as a value/values")

    return desc
