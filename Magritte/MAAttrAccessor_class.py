from MAAccessor_class import MAAccessor


class MAAttrAccessor(MAAccessor):

    def __init__(self, aAttrName):
        self._attrName = aAttrName

    @classmethod
    def isAbstract(cls):
        return False

    def canRead(self, aModel):
        attr = getattr(aModel.__class__, self._attrName, None)
        if attr:
            if isinstance(attr, property):
                return attr.fget is not None
            else:
                return False
        attr = getattr(aModel, self._attrName, None)
        return attr is not None

    def canWrite(self, aModel):
        attr = getattr(aModel.__class__, self._attrName, None)
        if attr:
            if isinstance(attr, property):
                return attr.fset is not None
            else:
                return False
        attr = getattr(aModel, self._attrName, None)
        return attr is not None


    @property
    def name(self):
        return self._attrName

    def read(self, aModel):
        return getattr(aModel, self._attrName)

    def write(self, aModel, anObject):
        setattr(aModel, self._attrName, anObject)
