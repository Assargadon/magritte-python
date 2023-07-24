
from sys import intern
from MAElementDescription_class import MAElementDescription

class MAStringDescription(MAElementDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def defaultKind(self):
        return str

    @classmethod
    def defaultLabel(self):
        return intern('str')

    def isSortable(self):
        return True
