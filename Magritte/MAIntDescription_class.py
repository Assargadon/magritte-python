from MANumberDescription_class import MANumberDescription
from sys import intern


class MAIntDescription(MANumberDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return int

