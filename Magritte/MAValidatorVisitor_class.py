
from MAVisitor_class import MAVisitor


class MAValidatorVisitor(MAVisitor):

    def __init__(self):
        self._object = None
        self._errors = []

    def useDuring(self, anObject, aBlock):
        previous = self._object
        self._object = anObject
        try:
            aBlock()
        except Exception:
            raise
        finally:
            self._object = previous

    def validateUsing(self, anObject, aDescription):
        self._errors = []
        self._errors += aDescription._validateRequired(anObject)
        if anObject == aDescription.undefinedValue:
            return self._errors
        errors = aDescription._validateKind(anObject)
        if errors:
            self._errors += errors
            return self._errors
        errors = aDescription._validateSpecific(anObject)
        if errors:
            self._errors += errors
            return self._errors
        errors = aDescription._validateConditions(anObject)
        if errors:
            self._errors += errors
            return self._errors
        return self._errors

    def visit(self, aDescription):
        if aDescription.isVisible and not aDescription.isReadOnly:
            super().visit(aDescription)

    def visitContainer(self, aDescription):
        super().visitContainer(aDescription)
        anObject = self._object
        if anObject is not None:
            for description in aDescription:
                self.useDuring(anObject.readUsing(description), lambda: self.visit(description))

    def visitDescription(self, aDescription):
        self._errors += self.validateUsing(self, aDescription)

