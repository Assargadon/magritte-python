from MANumberDescription_class import MANumberDescription
from sys import intern


class MAFloatDescription(MANumberDescription):

    def beInteger(self):
        self.addCondition(condition = lambda f: f.is_integer(),
                            label="Integer value required")  

    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return float

    def acceptMagritte(self, aVisitor):
        aVisitor.visitFloatDescription(self)
