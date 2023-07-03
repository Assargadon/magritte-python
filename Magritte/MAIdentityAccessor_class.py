from MAAccessor_class import MAAccessor


class MAIdentityAccessor(MAAccessor):

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        return True

    def read(self, aModel):
        return aModel

    def write(self, aModel, anObject):
        raise Exception("Not supposed to write to " + str(aModel) + ".")
