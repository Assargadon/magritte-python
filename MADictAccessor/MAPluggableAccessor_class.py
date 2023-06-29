from MAAccessor_class import MAAccessor


class MAPluggableAccessor(MAAccessor):

    def __init__(self, aReadFunc, aWriteFunc):
        self._readFunc = aReadFunc
        self._writeFunc = aWriteFunc

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        if (self._readFunc != None):
            return self._readFunc
        else:
            return None

    def canWrite(self, aModel):
        if (self._writeFunc != None):
            return self._writeFunc
        else:
            return None

    @property
    def readFunc(self):
        return self._readFunc

    @readFunc.setter
    def readFunc(self, aFunc):
        self._readFunc = aFunc

    @property
    def writeFunc(self):
        return self._writeFunc

    @writeFunc.setter
    def writeFunc(self, aFunc):
        self._writeFunc = aFunc

    def read(self, aModel):
        return self._readFunc(aModel)

    def write(self, aModel, anObject):
        self._writeFunc(aModel, anObject)
