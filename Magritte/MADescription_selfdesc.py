from sys import intern
from MAPriorityContainer_class import MAPriorityContainer
from MAElementDescription_class import MAElementDescription
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MABooleanDescription_class import MABooleanDescription
from MAToOneRelationDescription_class import MAToOneRelationDescription


def magritteDescription(self):
    desc = MAPriorityContainer()
    
    desc += MAStringDescription(label = "Kind", priority = 0, readOnly = True, accessor = intern('type'))
    desc += MAStringDescription(label = "Field name", priority = 1, accessor = intern('name'), comment = "Non-human-readable name, something like 'field name' or `json key`, etc.")
    desc += MAStringDescription(label = "Label", priority = 100, default = "#nolabel#", required = True, accessor = intern('label'))
    desc += MAStringDescription(label = "Group", priority = 105, default = self.defaultGroup(), accessor = intern('group'))
    desc += MAStringDescription(label = "Comment", priority = 110, default = self.defaultComment(), accessor = intern('comment'))
    desc += MAIntDescription(label = "Priority", priority = 130, default = self.defaultPriority(), required = True, accessor = intern('priority'))
    desc += MAStringDescription(label = "Undefined String", priority = 140, default = self.defaultUndefined(), accessor = intern('undefined'), comment = "A string that is printed whenever the model described by the receiver is None.")
    desc += MABooleanDescription(label = 'Read-only', priority = 200, default = self.defaultReadOnly(), accessor = intern('readOnly'))
    desc += MABooleanDescription(label = 'Visible', priority = 210, default = self.defaultVisible(), accessor = intern('visible'))
    desc += MABooleanDescription(label = 'Required', priority = 220, default = self.defaultRequired(), accessor = intern('required'))

    # ========= special ==========    
    # originally in smalltalk #validator is MASingleOptionDescription with reference of MAClassDescription type
    # but as long as we only have one common-purpose validator, and as long as we have no MAClassDescription (yet?) I did it this way
    desc += MAElementDescription(label = 'Validator', priority = 250, default = self.defaultValidator(), accessor = intern('validator'))

    desc += MAElementDescription(label = "Accessor", priority = 10, accessor = intern('accessor'))
    desc += MAElementDescription(label = "Undefined Value", priority = 150, default = self.defaultUndefinedValue(), accessor = intern('undefinedValue'), comment = "Value, which is treated as, well, undefined. No need for it to be of the same kind to the kind of descriptor. Used to effectively override None - for example, if None is used as meaningful value.")
    # ========= /special ==========    

    return desc
