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

    @default.setter
    def default(self, anObject):
        self._default = anObject

    @classmethod
    def defaultDefault(cls):
        return None


    def acceptMagritte(self, aVisitor):
        aVisitor.visitElementDescription(self)
    
    def readString(self, aModel):
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringWriterVisitor
        writer = MAStringWriterVisitor()
        return writer.write_str(model=aModel, description=self)

    def writeString(self, aModel):
        from Magritte.visitors.MAStringWriterReader_visitors import MAStringReaderVisitor
        reader = MAStringReaderVisitor()
        return reader.read_str(model=aModel, description=self)