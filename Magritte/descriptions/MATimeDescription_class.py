from datetime import time

from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription


class MATimeDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return time

    def acceptMagritte(self, aVisitor):
        aVisitor.visitTimeDescription(self)