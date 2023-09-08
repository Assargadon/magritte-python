
from MAOptionDescription_class import MAOptionDescription

class MASingleOptionDescription(MAOptionDescription):

    def acceptMagritte(self, aVisitor):
        aVisitor.visitSingleOptionDescription(self)
