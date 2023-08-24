from MAError import MAError


class MAValidationError(MAError):
    def __init__(self, aDescription, aString):
        self.description = aDescription
        self.message = aString

    def __str__(self):
        return self.message

    def isResumable(self):
        while True:
            try:
                value = yield
            except Exception as e:
                print("Error:", e)
                value = None
            yield value

    def setDescription(self, aDescription):
        self.description = aDescription
