
from sys import intern
from MADescription_class import MADescription

class MAElementDescription(MADescription):

    @property
    def default(self):
        return self.get(intern('default'), self.defaultDefault())

    @default.setter
    def default(self, anObject):
        self[intern('default')] = anObject
