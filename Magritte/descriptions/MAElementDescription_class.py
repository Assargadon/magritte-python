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
    def sa_isPrimaryKey(self):
        try:
            return self._sa_isPrimaryKey
        except AttributeError:
            return self.sa_defaultIsPrimaryKey()

    @sa_isPrimaryKey.setter
    def sa_isPrimaryKey(self, aBool):
        self._sa_isPrimaryKey = aBool

    def sa_defaultIsPrimaryKey(self):
        return False

    @property
    def sa_attrName(self):
        """SQLAlchemy requires "physical" attribute for its models."""

        try:
            return self._sa_attr_name
        except AttributeError:
            return self._name

    @sa_attrName.setter
    def sa_attrName(self, aSymbol):
        if aSymbol is None:
            self._sa_attr_name = None
        else:
            self._sa_attr_name = intern(aSymbol)

    @property
    def sa_fieldName(self):
        try:
            return self._sa_field_name
        except AttributeError:
            return self._name

    @sa_fieldName.setter
    def sa_fieldName(self, aSymbol):
        if aSymbol is None:
            self._sa_field_name = None
        else:
            self._sa_field_name = intern(aSymbol)

    @property
    def sa_storable(self):
        try:
            return self._sa_storable
        except AttributeError:
            return self.sa_defaultStorable()

    @sa_storable.setter
    def sa_storable(self, aBool):
        self._sa_storable = aBool

    def sa_defaultStorable(self):
        return not self.readOnly

    def acceptMagritte(self, aVisitor):
        aVisitor.visitElementDescription(self)

    def writeString(self, aModel):
        return self.stringWriter.write_str(model=aModel, description=self)

    def readString(self, aModel):
        return self.stringReader.read_str(model=aModel, description=self)