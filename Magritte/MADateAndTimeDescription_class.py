from MAMagnitudeDescription_class import MAMagnitudeDescription
from datetime import datetime


class MADateAndTimeDescription(MAMagnitudeDescription):

    @classmethod
    def defaultKind(cls):
        return datetime

    @classmethod
    def isAbstract(cls):
        return False

