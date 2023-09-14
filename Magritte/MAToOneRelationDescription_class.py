
from MARelationDescription_class import MARelationDescription
from errors.MAKindError import MAKindError


class MAToOneRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitToOneRelationDescription(self)

    # =========== validation ===========

    def _validateKind(self, model):
        errors = super()._validateKind(model)
        if len(errors) > 0:
            return errors
        if not any(isinstance(model, cls) for cls in self.classes):
            return [MAKindError(aDescription=self, message=self.kindErrorMessage)]
        return []

    # =========== /validation ===========