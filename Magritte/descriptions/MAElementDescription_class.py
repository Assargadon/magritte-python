from Magritte.descriptions.MADescription_class import MADescription


class MAElementDescription(MADescription):
    def __init__(self, stringReader=None, stringWriter=None, **kwargs):
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringReaderVisitor
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringWriterVisitor
        if not stringReader:
            self.stringReader = MAStringReaderVisitor()
        if not stringWriter:
            self.stringWriter = MAStringWriterVisitor()
        super().__init__(**kwargs)

    def magritteDescription(self):
        from Magritte.descriptions import MAElementDescription_selfdesc
        return MAElementDescription_selfdesc.magritteDescription(self, super().magritteDescription())


    @property
    def default(self):
        try:
            return self._default
        except AttributeError:
            return self.defaultDefault()

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