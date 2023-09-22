
from sys import intern

class MAModel:

    @classmethod
    def readUsingWrapper(cls, model, description):
        if hasattr(model, intern('readUsing')):
            readUsing = getattr(model, intern('readUsing'))
            return readUsing(description)
        result = description.accessor.read(model)
        return description.undefinedValue if result is None else result

    @classmethod
    def writeUsingWrapper(cls, model, description, value):
        if hasattr(model, intern('writeUsing')):
            writeUsing = getattr(model, intern('writeUsing'))
            return writeUsing(description, value)
        description.accessor.write(model, value)

    def readUsing(self, description):
        result = description.accessor.read(self)
        return description.undefinedValue if result is None else result

    def writeUsing(self, description, value):
        description.accessor.write(self, value)
