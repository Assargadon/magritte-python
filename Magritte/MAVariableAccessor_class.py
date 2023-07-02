from MAAccessor_class import MAAccessor


class MAVariableAccessor(MAAccessor):

    def __init__(self, aString):
        self._name = aString

    @classmethod
    def isAbstract(cls):
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, aString):
        self._name = aString

    def canRead(self, aModel):
        all_attrs = dir(aModel)
        prop_attrs = [attr for attr in all_attrs if isinstance(getattr(type(aModel), attr, None), property)]
        if (self._name in prop_attrs):
            return True
        else:
            return False

    def canWrite(self, aModel):
        return self.canRead(aModel)

    def read(self, aModel):
        all_attrs = dir(aModel)
        prop_attrs = [attr for attr in all_attrs if isinstance(getattr(type(aModel), attr, None), property)]
        if (self._name in prop_attrs):
            return object.__getattribute__(aModel, self._name)
        else:
            return None

    def write(self, aModel, anObject):
        all_attrs = dir(aModel)
        prop_attrs = [attr for attr in all_attrs if isinstance(getattr(type(aModel), attr, None), property)]
        if (self._name in prop_attrs):
            setattr(aModel, self._name, anObject)
        else:
            return None
