from datetime import datetime

from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription


class MADateAndTimeDescription(MAMagnitudeDescription):

    @classmethod
    def defaultKind(cls):
        return datetime

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        return aVisitor.visitDateAndTimeDescription(self)
