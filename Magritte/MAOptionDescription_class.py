
from sys import intern
from copy import copy
from MAReferenceDescription_class import MAReferenceDescription

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
        return self.get(intern('extensible'), self.defaultExtensible())

    @extensible.setter
    def extensible(self, aBoolean):
        self[intern('extensible')] = aBoolean

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
        return self.get(intern('sorted'), self.defaultExtensible())

    @sorted.setter
    def sorted(self, aBoolean):
        self[intern('sorted')] = aBoolean

    def beSorted(self):
        self.sorted = True

    def beUnsorted(self):
        self.sorted = False

    @property
    def undefined(self):
        return super().undefined

    @undefined.setter
    def undefined(self, aStr):
        super().undefined = aStr
        if self.reference is not None:
            self.reference.undefined = aStr

