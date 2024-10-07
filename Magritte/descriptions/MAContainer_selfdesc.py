from sys import intern

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription


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

    ancestor_desc = MAToOneRelationDescription(
        name=intern('ancestor'),
        label="Ancestor",
        priority=300,
        default=None,
        classes=[MAContainer],
        reference = desc,
        accessor = MAAttrAccessor('ancestor')
    )

    desc += ancestor_desc
    
    return desc
