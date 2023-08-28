from MAError import MAError


class MAValidationError(MAError):
    def __init__(self, aDescription, aString):
        self.description = aDescription
        self.message = aString

    def __str__(self):
        return self.message
