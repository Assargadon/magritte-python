from MAAccessor_class import MAAccessor


class MAVariableAccessor(MAAccessor):

    def __init__(self, aString):
        self._name = aString

    @classmethod
    def isAbstract(cls):
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, aString):
        self._name = aString

    def canRead(self, aModel):
        return hasattr(aModel, self._name)

    def canWrite(self, aModel):
        return self.canRead(aModel)

    def read(self, aModel):
        if (self.canRead(aModel)):
            return object.__getattribute__(aModel, self._name)
        else:
            return None

    def write(self, aModel, anObject):
        if (self.canRead(aModel)):
            setattr(aModel, self._name, anObject)
        else:
            return None
