from MAValidationError import MAValidationError


class MAMultipleErrors(MAValidationError):
    def __init__(self, aDescription, aCollection, aString):
        super().__init__(aDescription, aString)
        self.collection = aCollection
