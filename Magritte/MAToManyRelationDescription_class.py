from collections.abc import Sequence

from MARelationDescription_class import MARelationDescription
from errors.MARequiredError import MARequiredError

class MAToManyRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    # =========== validation ===========
    
    def _validateRequired(self, model):
        errors = super()._validateRequired(model)
        if len(errors) > 0:
            return errors
        if self.isRequired() and isinstance(model, Sequence) and len(model) == 0:
            return [MARequiredError(message = self.requiredErrorMessage, aDescription = self)]
        else:
            return []

    # =========== /validation ===========

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToManyRelationDescription(self)
