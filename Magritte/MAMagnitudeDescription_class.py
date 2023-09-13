from sys import intern
from MAElementDescription_class import MAElementDescription
from errors.MARangeError import MARangeError

class MAMagnitudeDescription(MAElementDescription):


    def isSortable(self):
        return True


    def isWithinRange(self, anObject):
        return (self.min is None or self.min <= anObject) and (self.max is None or self.max >= anObject)


    @property
    def max(self):
        try:
            return self._max
        except AttributeError:
            return self.defaultMax()

    @max.setter
    def max(self, anObjectOrNone):
        self._max = anObjectOrNone

    @classmethod
    def defaultMax(cls):
        return None

    @property
    def min(self):
        try:
            return self._min
        except AttributeError:
            return self.defaultMin()

    @min.setter
    def min(self, anObjectOrNone):
        self._min = anObjectOrNone

    @classmethod
    def defaultMin(cls):
        return None

    def setMinMax(self, aMinimumObject, aMaximumObject):
        self.min = aMinimumObject
        self.max = aMaximumObject

    # =========== attributes-messages-validation ===========

    @property
    def rangeErrorMessage(self):
        try:
            return self._rangeErrorMessage
        except AttributeError:
            min = self.min
            max = self.max
            if min is not None:
                if max is not None:
                    defaultRangeErrorMessage = f'Input must be between {min} and {max}'
                else:
                    defaultRangeErrorMessage = f'Input must be above or equal to {min}'
            else:
                if max is not None:
                    defaultRangeErrorMessage = f'Input must be below or equal to {max}'
                else:
                    defaultRangeErrorMessage = None
            return defaultRangeErrorMessage

    @rangeErrorMessage.setter
    def rangeErrorMessage(self, aString):
        self._rangeErrorMessage = aString

    # =========== /attributes-messages-validation ===========

    # =========== validation ===========
    
    def _validateSpecific(self, model):
        if(not self.isWithinRange(model)):
            return [
                *super()._validateSpecific(model),
                MARangeError(message = self.rangeErrorMessage, aDescription = self)
            ]
        else:
            return super()._validateSpecific(model)

    # =========== /validation ===========

    def acceptMagritte(self, aVisitor):
        aVisitor.visitMagnitudeDescription(self)
