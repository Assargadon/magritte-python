from sys import intern
from MAStringDescription_class import MAStringDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += MAStringDescription(label='False String', priority=410, default=self.defaultFalseString(), accessor=intern('falseString'))
    desc += MAStringDescription(label='True String', priority=400, default=self.defaultTrueString(), accessor=intern('trueString'))

    return desc
