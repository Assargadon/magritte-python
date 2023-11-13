import random

from accessors.MAAccessor_class import MAAccessor


class MANullAccessor(MAAccessor):

    def __init__(self):
        self._uuid = [random.randint(0, 255) for _ in range(16)]

    @classmethod
    def isAbstract(cls):
        return False

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, anObject):
        self._uuid = anObject

    def __eq__(self, other):
        return self._uuid == other._uuid

    def __hash__(self):
        return hash(tuple(self._uuid))

    def read(self, aModel):
        raise Exception(".read(...) is not appropriate for MANullAccessor")

    def write(self, aModel, anObject):
        raise Exception(".write(...) is not appropriate for MANullAccessor")
