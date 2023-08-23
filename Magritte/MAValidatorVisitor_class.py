
from MAVisitor_class import MAVisitor


class MAValidatorVisitor(MAVisitor):

    def __init__(self):
        self.object = None

    def onDescription(self, anObject, aDescription):
        self.useDuring(anObject, lambda : self.visit(aDescription))

    def useDuring(self, anObject, aBlock):
        previous = self.object
        self.object = anObject
        try:
            aBlock()
        except Exception:
            raise
        finally:
            self.object = previous

    def validateUsing(self, anObject, aDescription):
        aDescription.validateRequired(anObject)
        if anObject == aDescription.undefinedValue:
            return
        aDescription.tryValidation(lambda : aDescription.validateKind(anObject), lambda : (aDescription.validateSpecific(anObject), aDescription.validateConditions(anObject)))

    def visit(self, aDescription):
        if aDescription.isVisible and not aDescription.isReadOnly:
            super().visit(aDescription)

    def visitContainer(self, aDescription):
        super().visitContainer(aDescription)
        anObject = self.object
        if anObject is not None:
            self.useDuring(anObject.readUsing(aDescription), lambda : self.visit(aDescription))

    def visitDescription(self, aDescription):
        self.validateUsing(self, aDescription)

