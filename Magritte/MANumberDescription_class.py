from MAMagnitudeDescription_class import MAMagnitudeDescription


class MANumberDescription(MAMagnitudeDescription):
    @classmethod
    def isAbstract(cls):
        return True

    def acceptMagritte(self, aVisitor):
        aVisitor.visitNumberDescription(self)
