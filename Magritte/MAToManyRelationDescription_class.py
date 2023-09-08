
from MARelationDescription_class import MARelationDescription

class MAToManyRelationDescription(MARelationDescription):

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToManyRelationDescription(self)
