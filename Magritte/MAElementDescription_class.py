
from sys import intern
from MADescription_class import MADescription

class MAElementDescription(MADescription):

    def magritteDescription(self):
        import MAElementDescription_selfdesc
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
