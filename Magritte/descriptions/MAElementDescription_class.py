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

    @default.setter
    def default(self, anObject):
        self._default = anObject

    @classmethod
    def defaultDefault(cls):
        return None

    def acceptMagritte(self, aVisitor):
        aVisitor.visitElementDescription(self)

    def writeString(self, aModel):
        return self.stringWriter.write_str(model=aModel, description=self)

    def readString(self, aModel):
        return self.stringReader.read_str(model=aModel, description=self)