from accessors.MAAttrAccessor_class import MAAttrAccessor
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAElementDescription_class import MAElementDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription

# ======== special ==========
    desc += MAElementDescription(
        name="classes",
        label="Classes which fit to the relation",
        priority=400,
        default=self.defaultClasses(),
        accessor = MAAttrAccessor("classes")
    )
# ======== /special ==========
    
    return desc
