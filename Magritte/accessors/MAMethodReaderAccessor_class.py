from . MAAccessor_class import MAAccessor

class MAMethodReaderAccessor(MAAccessor):

    def __init__(self, aMethodName):
        self._methodName = aMethodName

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        attr = getattr(aModel, self._methodName, None)
        if not attr:
            return False

        return  callable(attr)

    def canWrite(self, aModel):
        return False

    @property
    def name(self):
        return self._methodName

    def read(self, aModel):
        reader_method = getattr(aModel, self._methodName, None)
        if not reader_method:
            return None
        if not callable(reader_method):
            return None
        return reader_method()

