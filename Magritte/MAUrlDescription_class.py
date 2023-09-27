from MAElementDescription_class import MAElementDescription


class MAUrlDescription(MAElementDescription):

    def acceptMagritte(self, aVisitor):
        aVisitor.visitUrlDescription(self)