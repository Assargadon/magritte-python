from datetime import timedelta

from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription


class MADurationDescription(MAMagnitudeDescription):

    @classmethod
    def defaultKind(cls):
        return timedelta

    @classmethod
    def isAbstract(cls):
        return False
    
    @classmethod
    def defaultDurationFormating(cls):
        return cls.defaultDurationForms()[0]

    @classmethod
    def defaultDurationForms(cls):
        return ['%d days, %H:%M:%S', '%H:%M:%S']

    def acceptMagritte(self, aVisitor):
        aVisitor.visitDurationDescription(self)
