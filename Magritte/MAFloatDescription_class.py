from MANumberDescription_class import MANumberDescription
from sys import intern


class MAFloatDescription(MANumberDescription):

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return float

