
from MAOptionDescription_class import MAOptionDescription

class MASingleOptionDescription(MAOptionDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitSingleOptionDescription(self)
