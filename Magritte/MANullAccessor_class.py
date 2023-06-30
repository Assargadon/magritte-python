from MAAccessor_class import MAAccessor
import random


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

    def read(self, aModel):
        return Exception("This message is not appropriate for this object")

    def write(self, aModel, anObject):
        return Exception("This message is not appropriate for this object")


# m = MANullAccessor()
# d = {1:1, 2:2, 3:3}
# print(m.uuid)
# print(m.read(d))
# print(m.write(d, 3))
# print(type(m.uuid))