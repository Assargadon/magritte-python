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

    @property
    def name(self):
        return None

    def read(self, aModel):
        return None

    def write(self, aModel, anObject):
        pass