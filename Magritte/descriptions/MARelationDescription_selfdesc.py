from sys import intern

from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription


def magritteDescription(self, parentDescription):
    desc = parentDescription

# ======== special ==========
    desc += MAElementDescription(
        label="Classes which fit to the relation",
        priority=400,
        default=self.defaultClasses(),
        accessor=intern('classes')
    )
    desc += MAStringDescription(
        label="Name of the relationship for disambiguation in case of multiple bidirectional relations",
        priority=410,
        default=self.defaultRelationship(),
        accessor=intern('relationship')
    )
# ======== /special ==========
    
    return desc
