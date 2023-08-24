from MAError import MAError


class MAValidationError(MAError):
    def __init__(self, aDescription, aString):
        self._description = aDescription
        self._string = aString

    @classmethod
    def isResumable(cls):
        return True

    def setDescription(self, aDescription):
        self._description = aDescription
