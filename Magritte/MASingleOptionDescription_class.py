
from MAOptionDescription_class import MAOptionDescription

class MASingleOptionDescription(MAOptionDescription):

    @property
    def groupBy(self):
        try:
            return self._groupBy
        except AttributeError:
            return None

    @groupBy.setter
    def groupBy(self, anMAAccessor):
        self._groupBy = anMAAccessor

    def isGrouped(self):
        try:
            return self._groupBy is not None
        except AttributeError:
            return False

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
