from MAAccessor_class import MAAccessor


class MAPluggableAccessor(MAAccessor):

    def __init__(self, aReadBlock, aWRiteBlock):
        self._readBlock = aReadBlock
        self._writeBlock = aWRiteBlock

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        if (self._readBlock != None):
            return self._readBlock
        else:
            return None

    def canWrite(self, aModel):
        if (self._writeBlock != None):
            return self._writeBlock
        else:
            return None

    @property
    def readBlock(self):
        return self._readBlock

    @readBlock.setter
    def readBlock(self, newReadBlock):
        self._readBlock = newReadBlock

    @property
    def writeBlock(self):
        return self._writeBlock

    @writeBlock.setter
    def writeBlock(self, newWriteBlock):
        self._writeBlock = newWriteBlock

    def read(self, aModel):
        return aModel.get(self.readBlock)

    def write(self, aModel, anObject):
        aModel[self.writeBlock] = anObject
