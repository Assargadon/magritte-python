
from sys import intern
from MAElementDescription_class import MAElementDescription

class MAMagnitudeDescription(MAElementDescription):


    def isSortable(self):
        return True


    def isWithinRange(self, anObject):
        return (self.min is None or self.min <= anObject) and (self.max is None or self.max >= anObject)


    @property
    def max(self):
        return self.get(intern('max'), self.defaultMax())

    @max.setter
    def max(self, anObjectOrNone):
        self[intern('max')] = anObjectOrNone

    @classmethod
    def defaultMax(cls):
        return None

    @property
    def min(self):
        return self.get(intern('min'), self.defaultMin())

    @min.setter
    def min(self, anObjectOrNone):
        self[intern('min')] = anObjectOrNone

    @classmethod
    def defaultMin(cls):
        return None

    def setMinMax(self, aMinimumObject, aMaximumObject):
        self.min = aMinimumObject
        self.max = aMaximumObject


    @property
    def rangeErrorMessage(self):
        min = self.min
        max = self.max
        if min is not None:
            if max is not None:
                defaultRangeErrorMessage = f'Input must be between {min} and {max}'
            else:
                defaultRangeErrorMessage = f'Input must be above or equeal to {min}'
        else:
            if max is not None:
                defaultRangeErrorMessage = f'Input must be below or eqeal to {max}'
            else:
                defaultRangeErrorMessage = None
        return self.get(intern('rangeErrorMessage'), defaultRangeErrorMessage)

    @rangeErrorMessage.setter
    def rangeErrorMessage(self, aString):
        self[intern('rangeErrorMessage')] = aString


    def acceptMagritte(self, aVisitor):
        aVisitor.visitMagnitudeDescription(self)
