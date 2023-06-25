from MAAccessor_class import MAAccessor


class MADictAccessor(MAAccessor):

    def __init__(self, aSymbol):
        self.key = aSymbol

    @property
    def getKey(self):
        return self.key

    @getKey.setter
    def setKey(self, newKey):
        self.key = newKey

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        return True

    def canWrite(self, aModel):
        return True

    def read(self, aModel):
        if (self.key in aModel):
            return aModel[self.key]
        else:
            return False

    def write(self, aModel, anObject):
        aModel[self.key] = anObject