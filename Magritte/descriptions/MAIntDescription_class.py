from Magritte.descriptions.MANumberDescription_class import MANumberDescription


class MAIntDescription(MANumberDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return int

    def acceptMagritte(self, aVisitor):
        return aVisitor.visitIntDescription(self)
