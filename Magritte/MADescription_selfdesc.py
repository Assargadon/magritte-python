from MAPriorityContainer_class import MAPriorityContainer
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MABooleanDescription_class import MABooleanDescription

from accessors.MAAttrAccessor_class import MAAttrAccessor

def magritteDescription(self):
    desc = MAPriorityContainer()
    
    desc += MAStringDescription(label = "Label", priority = 100, default = "#nolabel#", required = True, accessor = MAAttrAccessor('label'))
    desc += MAIntDescription(label = "Priority", priority = 130, default = self.defaultPriority(), required = True, accessor = MAAttrAccessor('priority'))
    desc += MABooleanDescription(label = 'Read-only', priority = 200, default = self.defaultReadOnly(), accessor = MAAttrAccessor('readOnly'))
    desc += MABooleanDescription(label = 'Visible', priority = 210, default = self.defaultVisible(), accessor = MAAttrAccessor('visible'))
    desc += MABooleanDescription(label = 'Required', priority = 220, default = self.defaultRequired(), accessor = MAAttrAccessor('required'))
    return desc
    
