from MAMagnitudeDescription_class import MAMagnitudeDescription
from datetime import timedelta


class MADurationDescription(MAMagnitudeDescription):

    @classmethod
    def defaultKind(cls):
        return timedelta

    @classmethod
    def isAbstract(cls):
        return False

    @property
    def label(self):
        return "Duration"
