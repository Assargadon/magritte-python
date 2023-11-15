from Magritte.descriptions.MAStringDescription_class import MAStringDescription


class MAMemoDescription(MAStringDescription):

    def defaultLineCount(self):
        return 3

    @property
    def lineCount(self):
        try:
            return self._lineCount
        except AttributeError:
            return self.defaultLineCount()

    @lineCount.setter
    def lineCount(self, anInteger):
        self._lineCount = anInteger

    def acceptMagritte(self, aVisitor):
        aVisitor.visitMemoDescription(self)
