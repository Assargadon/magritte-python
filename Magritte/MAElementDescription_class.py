
from sys import intern
from MADescription_class import MADescription

class MAElementDescription(MADescription):

    @property
    def default(self):
        return self._getOrDefaultIfAbsent(intern('default'), self.defaultDefault)

    @default.setter
    def default(self, anObject):
        self._set(intern('default'), anObject)

    def acceptMagritte(self, aVisitor):
        aVisitor.visitElementDescription(self)
