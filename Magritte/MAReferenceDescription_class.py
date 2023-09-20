
from copy import copy
from sys import intern
from MAElementDescription_class import MAElementDescription
from MAStringDescription_class import MAStringDescription

class MAReferenceDescription(MAElementDescription):

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.reference = copy(self.reference)
        return clone

    def magritteDescription(self):
        import MAReferenceDescription_selfdesc
        return MAReferenceDescription_selfdesc.magritteDescription(self, super().magritteDescription())

    @classmethod
    def defaultReference(cls):
        return MAStringDescription()

    @property
    def reference(self):
        try:
            if self._reference is None:
                self._reference = self.defaultReference()
        except AttributeError:
            self._reference = self.defaultReference()
 
        return self._reference
        

    @reference.setter
    def reference(self, aDescription):
        self._reference = aDescription

    def acceptMagritte(self, aVisitor):
        aVisitor.visitReferenceDescription(self)
