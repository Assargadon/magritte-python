from MAAccessor_class import MAAccessor


class MAPluggableAccessor(MAAccessor):

    def __init__(self, aReadBlock, aWriteBlock):
        self._readBlock = lambda aReadBlock: aReadBlock
        self._writeBlock = lambda aReadBlock, aWriteBlock: aReadBlock.setdefault('new', aWriteBlock)

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
    def readBlock(self, aBlock):
        self._readBlock = aBlock

    @property
    def writeBlock(self):
        return self._writeBlock

    @writeBlock.setter
    def writeBlock(self, aBlock):
        self._writeBlock = aBlock

    # def read(self, aModel):
    #     return aModel.get(self.readBlock)
    def read(self, aModel):
        return self._readBlock(aModel)

    def write(self, aModel, anObject):
        self._writeBlock(aModel, anObject)


d = {1: 10, 2: 11, 3: 13}
m = MAPluggableAccessor(d, 3)
m.write(d, 4)
print(m.read(d))
print(m.writeBlock)
# def multiply(num1):
#     var = 10
#     def inner(num2):
#         return num1 * num2
#     return inner
#
# mult = multiply(9)
# print(mult(3))
