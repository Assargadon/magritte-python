
from copy import copy

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.errors.MAKindError import MAKindError


class MAOptionDescription(MAReferenceDescription):

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.options = copy(self.options)
        return clone

    def magritteDescription(self):
        from Magritte.descriptions import MAOptionDescription_selfdesc
        return MAOptionDescription_selfdesc.magritteDescription(self, super().magritteDescription())

    @classmethod
    def defaultOptions(cls):
        return list()

    @property
    def options(self):
        try:
            return self._options
        except AttributeError:
            self._options = self.defaultOptions()
            return self._options

    @options.setter
    def options(self, anArray):
        self._options = anArray


    @classmethod
    def defaultExtensible(cls):
        return False

    @property
    def extensible(self):
        try:
            return self._extensible
        except AttributeError:
            return self.defaultExtensible()

    @extensible.setter
    def extensible(self, aBoolean):
        self._extensible = aBoolean

    def beExtensible(self):
        self.extensible = True

    def beLimited(self):
        self.extensible = False

    def isExtensible(self):
        return self.extensible

    @property
    def groupBy(self):
        try:
            return self._groupBy
        except AttributeError:
            return None

    @groupBy.setter
    def groupBy(self, anMAAccessor):
        self._groupBy = anMAAccessor

    def isGrouped(self):
        try:
            return self._groupBy is not None
        except AttributeError:
            return False



    @classmethod
    def defaultSorted(cls):
        return False

    @property
    def sorted(self):
        try:
            return self._sorted
        except AttributeError:
            return self.defaultSorted()

    @sorted.setter
    def sorted(self, aBoolean):
        self._sorted = aBoolean

    def beSorted(self):
        self.sorted = True

    def beUnsorted(self):
        self.sorted = False

    def isSorted(self):
        return self.sorted


    def _undefined_set(self, aStr):
        super()._undefined_set(aStr)
        if self.reference is not None:
            self.reference.undefined = aStr


    def acceptMagritte(self, aVisitor):
        aVisitor.visitOptionDescription(self)


    def _validateOptionKind(self, model):
        if model in self.options:
            return []
        if self.isExtensible():
            return self.reference.validate(model)
        else:
            return [MAKindError(aDescription=self, message=self.kindErrorMessage)]

    # =========== / validation ===========
