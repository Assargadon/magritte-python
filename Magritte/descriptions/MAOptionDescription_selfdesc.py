from sys import intern

from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from descriptions.MAElementDescription_class import MAElementDescription


def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MABooleanDescription(label='Sorted', priority=240, default=self.defaultSorted(), accessor=intern('sorted'))
    desc += MABooleanDescription(label='Extensible', priority=250, default=self.defaultExtensible(), accessor=intern('extensible'))
    desc += MAToManyRelationDescription(label="Options", priority=410, default=self.defaultOptions(), reference=self.reference, accessor=intern('options'))

    # ========= special ==========    
    desc += MAElementDescription(label = "Grouped By", priority = 260, accessor = intern('groupBy'), comment = "Accessor to retrieve value used for grouping of option objects out of these option objects")
    # ========= /special ==========    

    return desc
