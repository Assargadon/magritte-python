from accessors.MAIdentityAccessor_class import MAIdentityAccessor
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAElementDescription_class import MAElementDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MAToManyRelationDescription(
        name="children",
        label="Elements",
        priority=400,
        default=self.defaultCollection(),
        classes=[MAElementDescription],
        reference = MAElementDescription().magritteDescription(),
        accessor = MAIdentityAccessor()
    )
    
    return desc
