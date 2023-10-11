from . MAAccessor_class import MAAccessor

class MAMethodReaderAccessor(MAAccessor):

    def __init__(self, aMethodName):
        self._methodName = aMethodName

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        return getattr(aModel, self._methodName, None) is not None

    def canWrite(self, aModel):
        return False

    @property
    def name(self):
        return self._methodName

    def read(self, aModel):
        reader_method = getattr(aModel, self._methodName, None)
        return reader_method()

