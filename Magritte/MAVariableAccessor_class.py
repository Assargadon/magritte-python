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
            return getattr(aModel, self._name)

    def write(self, aModel, anObject):
        if (self.canWrite(aModel)):
            setattr(aModel, self._name, anObject)
