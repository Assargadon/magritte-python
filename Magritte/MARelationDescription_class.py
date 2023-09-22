
from copy import copy
from MAReferenceDescription_class import MAReferenceDescription
from MAPriorityContainer_class import MAPriorityContainer

class MARelationDescription(MAReferenceDescription):

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.classes = copy(self.classes)
        return clone

    @classmethod
    def defaultClasses(cls):
        return set()

    @property
    def classes(self):
        try:
            return self._classes
        except AttributeError:
            self._classes = self.defaultClasses()
            return self._classes

    @classes.setter
    def classes(self, aCollection):
        self._classes = aCollection

    def commonClass(self):
        if not self.classes:
            return None

        current = next(iter(self.classes))
        for item in self.classes:
            while not issubclass(item, current):
                current = current.__bases__[0]
        return current

    @property
    def reference(self):
        reference = super().reference
        if reference is None:
            commonClass = self.commonClass()
            if commonClass is None:
                descriptionContainer = self.defaultReference()
                descriptionContainer.label = self.label
                return descriptionContainer
            else:
                return commonClass.magritteTemplate.magritteDescription
        else:
            return reference

    @reference.setter
    def reference(self, aDescription):
        self._reference = aDescription

    @classmethod
    def defaultReference(cls):
        return MAPriorityContainer()

    def acceptMagritte(self, aVisitor):
        aVisitor.visitRelationDescription(self)
