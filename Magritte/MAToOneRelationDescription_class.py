
from MARelationDescription_class import MARelationDescription

class MAToOneRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToOneRelationDescription(self)
