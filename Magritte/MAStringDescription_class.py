
from sys import intern
from MAElementDescription_class import MAElementDescription

class MAStringDescription(MAElementDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return str

    def isSortable(self):
        return True


    def acceptMagritte(self, aVisitor):
        aVisitor.visitStringDescription(self)
