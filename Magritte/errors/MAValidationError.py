from MAError import MAError


class MAValidationError(MAError):
    def __init__(self, aDescription, message):
        self.description = aDescription
        self.message = message

    def __str__(self):
        return self.message
