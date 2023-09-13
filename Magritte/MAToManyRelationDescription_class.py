from collections.abc import Sequence

from MARelationDescription_class import MARelationDescription
from errors.MARequiredError import MARequiredError

class MAToManyRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    # =========== validation ===========
    
    def _validateRequired(self, model):
        superValidationResult = super()._validateRequired(model)
        if(superValidationResult): return superValidationResult
        
        if(self.isRequired and isinstance(model, Sequence) and not len(model)):
            return [MARequiredError(message = self.requiredErrorMessage, aDescription = self)]
        else:
            return []

    # =========== /validation ===========

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToManyRelationDescription(self)
