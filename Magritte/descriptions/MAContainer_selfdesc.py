from sys import intern

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAElementDescription_class import MAElementDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MAToManyRelationDescription(
        name=intern('children'),
        label="Elements",
        priority=400,
        default=self.defaultCollection(),
        classes=[MAElementDescription],
        reference = MAElementDescription().magritteDescription(),
        accessor = MAAttrAccessor('children')
    )
    
    return desc
