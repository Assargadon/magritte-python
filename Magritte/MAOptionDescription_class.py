
from copy import copy
from MAReferenceDescription_class import MAReferenceDescription
from errors.MAKindError import MAKindError

class MAOptionDescription(MAReferenceDescription):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._options = self.defaultOptions()

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.options = copy(self.options)
        return clone

    @classmethod
    def defaultOptions(cls):
        return list()

    @property
    def options(self):
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
        if model in self._options:
            return []
        if self.isExtensible():
            return self.reference.validate(model)
        else:
            return [MAKindError(aDescription=self, message=self.kindErrorMessage)]

    # =========== / validation ===========
