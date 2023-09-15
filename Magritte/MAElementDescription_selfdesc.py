from accessors.MAAttrAccessor_class import MAAttrAccessor
#from MAToManyRelationDescription_class import MAToManyRelationDescription
#from MAElementDescription_class import MAElementDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += self.__class__(label = 'Default', priority = 130, default = self.defaultDefault(), accessor = MAAttrAccessor("default"))

    return desc
