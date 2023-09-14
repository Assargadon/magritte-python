from MAPriorityContainer_class import MAPriorityContainer
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from accessors.MAAttrAccessor_class import MAAttrAccessor

def magritteDescription(self):
    desc = MAPriorityContainer()
    
    desc += MAStringDescription(label = "Label", priority = 100, default = "#nolabel#", required = True, accessor = MAAttrAccessor('label'))
    desc += MAIntDescription(label = "Priority", priority = 130, default = self.defaultPriority(), required = True, accessor = MAAttrAccessor('priority'))

    return desc
