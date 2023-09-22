from sys import intern
from MAToOneRelationDescription_class import MAToOneRelationDescription
from MADescription_class import MADescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MAToOneRelationDescription(label = "Description", priority = 400, classes = [MADescription], accessor = intern('reference'), comment = "Description of the dependent model used as a value/values")

    return desc
