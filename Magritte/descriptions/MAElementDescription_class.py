from sys import intern

from Magritte.descriptions.MADescription_class import MADescription


class MAElementDescription(MADescription):
    def magritteDescription(self):
        from Magritte.descriptions import MAElementDescription_selfdesc
        return MAElementDescription_selfdesc.magritteDescription(self, super().magritteDescription())

    @property
    def default(self):
        try:
            return self._default
        except AttributeError:
            return self.defaultDefault()

    @property
    def defaultStringReader(self):
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringReaderVisitor
        return MAStringReaderVisitor

    @property
    def defaultStringWriter(self):
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringWriterVisitor
        return MAStringWriterVisitor

    @property
    def stringWriter(self):
        try:
            return self._stringWriter
        except AttributeError:
            return self.defaultStringWriter()

    @property
    def stringReader(self):
        try:
            return self._stringReader
        except AttributeError:
            return self.defaultStringReader()

    @stringReader.setter
    def stringReader(self, anObject):
        self._stringReader = anObject

    @stringWriter.setter
    def stringWriter(self, anObject):
        self._stringWriter = anObject
        

    @default.setter
    def default(self, anObject):
        self._default = anObject

    @classmethod
    def defaultDefault(cls):
        return None

    @property
    def isPrimaryKey(self):
        try:
            return self._isPrimaryKey
        except AttributeError:
            return self.defaultIsPrimaryKey()

    @isPrimaryKey.setter
    def isPrimaryKey(self, aBool):
        self._isPrimaryKey = aBool

    def defaultIsPrimaryKey(self):
        return False

    @property
    def fieldName(self):
        try:
            return self._field_name
        except AttributeError:
            return self._name

    @fieldName.setter
    def fieldName(self, aSymbol):
        if aSymbol is None:
            self._field_name = None
        else:
            self._field_name = intern(aSymbol)

    def acceptMagritte(self, aVisitor):
        aVisitor.visitElementDescription(self)

    def writeString(self, aModel):
        return self.stringWriter.write_str(model=aModel, description=self)

    def readString(self, aModel):
        return self.stringReader.read_str(model=aModel, description=self)