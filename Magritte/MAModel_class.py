
class MAModel:

    def readUsing(self, description):
        result = description.accessor.read(self)
        return description.undefinedValue if result is None else result

    def writeUsing(self, description, value):
        description.accessor.write(self, value)
