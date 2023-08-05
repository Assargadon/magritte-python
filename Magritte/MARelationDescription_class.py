
from copy import copy
from MAReferenceDescription_class import MAReferenceDescription
from MAPriorityContainer_class import MAPriorityContainer

class MARelationDescription(MAReferenceDescription):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._classes = self.defaultClasses()

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
        return self._classes

    @classes.setter
    def classes(self, aCollection):
        self._classes = aCollection

    def commonClass(self):
        if len(self._classes) == 0:
            descriptionContainer = MAPriorityContainer()
            descriptionContainer.label = self.label
            return descriptionContainer
        current = next(iter(self.classes))
        for item in self.classes:
            while not issubclass(item, current):
                current = current.__bases__[0]
        return current

    def reference(self):
        reference = super().reference
        if reference is None:
            reference = self.commonClass().magritteTemplate.magritteDescription
        return reference


    def acceptMagritte(self, aVisitor):
        aVisitor.visitRelationDescription(self)
