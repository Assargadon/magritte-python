from datetime import date

from descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription


class MADateDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return date

    def acceptMagritte(self, aVisitor):
        aVisitor.visitDateDescription(self)
