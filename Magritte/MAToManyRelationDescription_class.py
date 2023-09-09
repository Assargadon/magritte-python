
from MARelationDescription_class import MARelationDescription

class MAToManyRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToManyRelationDescription(self)
