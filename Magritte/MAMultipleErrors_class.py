
class MAMultipleErrors(Exception):

    def __init__(self, errors=None, message=""):
        super().__init__(message)
        self._collection = errors if isinstance(errors, list) else []

    def __str__(self):
        stringArray = [str(element) for element in self._collection]
        return '\n'.join(stringArray)
