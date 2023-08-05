
from copy import copy
from sys import intern
from MAElementDescription_class import MAElementDescription
from MAStringDescription_class import MAStringDescription

class MAReferenceDescription(MAElementDescription):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._reference = self.defaultReference()

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.reference = copy(self.reference)
        return clone

    @classmethod
    def defaultReference(cls):
        return MAStringDescription()

    @property
    def initializer(self):
        return self.get(intern('initializer'), self)

    @initializer.setter
    def initializer(self, aValuable):
        self[intern('initializer')] = aValuable

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, aDescription):
        self._reference = aDescription


    def acceptMagritte(self, aVisitor):
        aVisitor.visitReferenceDescription(self)
