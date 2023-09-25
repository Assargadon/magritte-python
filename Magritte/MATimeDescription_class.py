from MAMagnitudeDescription_class import MAMagnitudeDescription
from datetime import time

class MATimeDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return time

    def acceptMagritte(self, aVisitor):
        aVisitor.visitTimeDescription(self)