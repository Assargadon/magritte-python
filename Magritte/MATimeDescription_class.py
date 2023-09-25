from MAMagnitudeDescription_class import MAMagnitudeDescription
from datetime import datetime

class MATimeDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return datetime

    def acceptMagritte(self, aVisitor):
        aVisitor.visitTimeDescription(self)