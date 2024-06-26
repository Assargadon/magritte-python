
from copy import copy
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription

class MAReferenceDescription(MAElementDescription):

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.reference = copy(self.reference)
        return clone

    def magritteDescription(self):
        from Magritte.descriptions import MAReferenceDescription_selfdesc
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

    def defaultReferenceAcyclic(self):
        return self.reference.acyclicDescription

    @property
    def referenceAcyclic(self):
        try:
            return self._referenceAcyclic
        except AttributeError:
            return self.defaultReferenceAcyclic()

    @referenceAcyclic.setter
    def referenceAcyclic(self, aDescription):
        self._referenceAcyclic = aDescription


    def acceptMagritte(self, aVisitor):
        aVisitor.visitReferenceDescription(self)
