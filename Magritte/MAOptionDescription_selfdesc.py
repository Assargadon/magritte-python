from accessors.MAAttrAccessor_class import MAAttrAccessor
from MAStringDescription_class import MAStringDescription
from MABooleanDescription_class import MABooleanDescription
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAElementDescription_class import MAElementDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MABooleanDescription(label='Sorted', priority=240, default=self.defaultSorted(), accessor=MAAttrAccessor('sorted'))
    desc += MABooleanDescription(label='Extensible', priority=250, default=self.defaultExtensible(), accessor=MAAttrAccessor('extensible'))
    desc += MAToManyRelationDescription(label = "Options", priority = 410, default = self.defaultOptions(), reference = self.reference, accessor = MAAttrAccessor('options'))

    # ========= special ==========    
    desc += MAElementDescription(label = "Grouped By", priority = 260, accessor = MAAttrAccessor('groupBy'), comment = "Accessor to retrieve value used for grouping of option objects out of these option objects")
    # ========= /special ==========    

    return desc
