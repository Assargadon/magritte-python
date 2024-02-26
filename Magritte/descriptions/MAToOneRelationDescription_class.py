from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.errors.MAKindError import MAKindError


class MAToOneRelationDescription(MARelationDescription):

    @classmethod
    def isAbstract(cls):
        return False

    def acceptMagritte(self, aVisitor):
        return aVisitor.visitToOneRelationDescription(self)

    # =========== validation ===========

    def _validateKind(self, model):
        errors = super()._validateKind(model)
        if errors:
            return errors
        if self.classes and not any(isinstance(model, cls) for cls in self.classes):
            return [MAKindError(aDescription=self, message=self.kindErrorMessage)]
        return []

    # =========== /validation ===========