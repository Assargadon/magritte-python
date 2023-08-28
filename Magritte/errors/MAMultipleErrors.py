from MAValidationError import MAValidationError


class MAMultipleErrors(MAValidationError):
    def __init__(self, aDescription, errors, message):
        super().__init__(aDescription, message)
        self.collection = errors
