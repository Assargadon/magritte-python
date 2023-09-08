
from MARelationDescription_class import MARelationDescription


class MAToOneRelationDescription(MARelationDescription):

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToOneRelationDescription(self)
