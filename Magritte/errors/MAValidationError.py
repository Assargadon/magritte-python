from Magritte.errors.MAError import MAError


class MAValidationError(MAError):
    def __init__(self, aDescription, message):
        self.description = aDescription
        self.message = message

    def __str__(self):
        return self.message

    # Just in case it will be useful somehow in future logic:
    # unlike Smalltalk, Python has no resumable exceptions  
    def isResumable(cls):
        return True
