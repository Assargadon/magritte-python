from MAAccessor_class import MAAccessor


class MADictAccessor(MAAccessor):

    def __init__(self, aSymbol):
        self._key = aSymbol

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, newKey):
        self._key = newKey

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        return True

    def canWrite(self, aModel):
        return True

    @property
    def name(self):
        return self._key

    def read(self, aModel):
        return aModel.get(self._key)

    def write(self, aModel, anObject):
        aModel[self._key] = anObject
