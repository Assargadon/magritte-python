from MAPriorityContainer_class import MAPriorityContainer
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MABooleanDescription_class import MABooleanDescription
from MAToOneRelationDescription_class import MAToOneRelationDescription

from accessors.MAAttrAccessor_class import MAAttrAccessor
from accessors.MAAccessor_class import MAAccessor

def magritteDescription(self):
    desc = MAPriorityContainer()
    
    desc += MAStringDescription(label = "Kind", priority = 0, readOnly = True, accessor = MAAttrAccessor('type'))
    desc += MAStringDescription(priority = 1, accessor = MAAttrAccessor('name'))
    desc += MAToOneRelationDescription(priority = 10, reference = MAStringDescription(), classes = [MAAccessor], accessor = MAAttrAccessor('accessor'), visible = False)
    desc += MAStringDescription(label = "Label", priority = 100, default = "#nolabel#", required = True, accessor = MAAttrAccessor('label'))
    desc += MAStringDescription(label = "Group", priority = 105, default = self.defaultGroup(), accessor = MAAttrAccessor('group'))
    desc += MAStringDescription(label = "Comment", priority = 110, default = self.defaultComment(), accessor = MAAttrAccessor('comment'))
    desc += MAIntDescription(label = "Priority", priority = 130, default = self.defaultPriority(), required = True, accessor = MAAttrAccessor('priority'))
    desc += MAStringDescription(label = "Undefined String", priority = 140, default = self.defaultUndefined(), accessor = MAAttrAccessor('undefined'), comment = "A string that is printed whenever the model described by the receiver is None.")
    desc += MABooleanDescription(label = 'Read-only', priority = 200, default = self.defaultReadOnly(), accessor = MAAttrAccessor('readOnly'))
    desc += MABooleanDescription(label = 'Visible', priority = 210, default = self.defaultVisible(), accessor = MAAttrAccessor('visible'))
    desc += MABooleanDescription(label = 'Required', priority = 220, default = self.defaultRequired(), accessor = MAAttrAccessor('required'))
    return desc
    

