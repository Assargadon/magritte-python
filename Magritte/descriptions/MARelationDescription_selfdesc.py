from sys import intern

from Magritte.descriptions.MAElementDescription_class import MAElementDescription


def magritteDescription(self, parentDescription):
    desc = parentDescription

# ======== special ==========
    desc += MAElementDescription(
        label="Classes which fit to the relation",
        priority=400,
        default=self.defaultClasses(),
        accessor=intern('classes')
    )
# ======== /special ==========
    
    return desc
