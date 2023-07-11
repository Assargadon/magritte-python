from MAAccessor_class import MAAccessor


class MASelectorAccessor(MAAccessor):

    def __init__(self, aReadSelector, aWriteSelector):
        self._readSelector = aReadSelector
        self._writeSelector = aWriteSelector

    @classmethod
    def isAbstract(cls):
        return False

    @property
    def readSelector(self):
        return self._readSelector

    @readSelector.setter
    def readSelector(self, aSelector):
        self._readSelector = aSelector

    @property
    def writeSelector(self):
        return self._writeSelector

    @writeSelector.setter
    def writeSelector(self, aSelector):
        self._writeSelector = aSelector

    def canRead(self, aModel):
        return hasattr(self, "_readSelector") and hasattr(aModel, self._readSelector)

    def canWrite(self, aModel):
        return hasattr(self, "_writeSelector") and hasattr(aModel, self._writeSelector)

    def read(self, aModel):
        try:
            return getattr(aModel, self._readSelector)()
        except:
            raise Exception("There is no such method")

    def write(self, aModel, anObject):
        try:
            return getattr(aModel, self._writeSelector)(anObject)
        except:
            raise Exception("There is no such method")
