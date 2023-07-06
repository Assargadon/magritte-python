
from MAElementDescription_class import MAElementDescription

class MAStringDescription(MAElementDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def defaultKind(self):
        return str

    def label(self):
        return 'String'

    def isSortable(self):
        return True

    def acceptMagritte(self, aVisitor):
        aVisitor.visitStringDescription(self)
