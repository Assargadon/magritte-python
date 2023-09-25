from MAMagnitudeDescription_class import MAMagnitudeDescription
from datetime import date

class MADateDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return date

    def acceptMagritte(self, aVisitor):
        aVisitor.visitDateDescription(self)
