from MAMagnitudeDescription_class import MAMagnitudeDescription
from MACondition import MACondition


class MANumberDescription(MAMagnitudeDescription):
    @classmethod
    def isAbstract(cls):
        return True

    def acceptMagritte(self, aVisitor):
        aVisitor.visitNumberDescription(self)
