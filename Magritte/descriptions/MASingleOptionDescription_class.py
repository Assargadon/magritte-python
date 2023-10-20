
from descriptions.MAOptionDescription_class import MAOptionDescription

class MASingleOptionDescription(MAOptionDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitSingleOptionDescription(self)


    # =========== validation ===========

    def _validateKind(self, model):
        errors = super()._validateKind(model)
        if errors:
            return errors
        errors = self._validateOptionKind(model)
        return errors

    # =========== / validation ===========
