class MAAccessor:

    def asAccessor(self):
        return self

    @classmethod
    def isAbstract(cls):
        return True

    def canRead(self, aModel):
        return False

    def canWrite(self, aModel):
        return False

    def read(self, aModel):
        return None

    def write(self, anObject, aModel):
        pass