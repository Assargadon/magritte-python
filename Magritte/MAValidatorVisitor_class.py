
from MAModel_class import MAModel
from MAVisitor_class import MAVisitor


class MAValidatorVisitor(MAVisitor):

    def __init__(self):
        self._object = None
        self._errors = []

    def validateModelDescription(self, aModel, aDescription):
        self._errors = []
        self.useDuring(aModel, lambda: self.visit(aDescription))
        return self._errors

    def useDuring(self, anObject, aBlock):
        previous = self._object
        self._object = anObject
        try:
            aBlock()
        except Exception as e:
            self._errors.append(e)
        finally:
            self._object = previous

    def validateUsing(self, anObject, aDescription):
        self._errors.extend(aDescription._validateRequired(anObject))
        if anObject == aDescription.undefinedValue:
            return
        errors = aDescription._validateKind(anObject)
        if errors:
            self._errors.extend(errors)
            return
        errors = aDescription._validateSpecific(anObject)
        if errors:
            self._errors.extend(errors)
            return
        errors = aDescription._validateConditions(anObject)
        if errors:
            self._errors.extend(errors)
            return

    def visit(self, aDescription):
        if aDescription.isVisible() and not aDescription.isReadOnly():
            super().visit(aDescription)

    def visitContainer(self, aDescription):
        super().visitContainer(aDescription)
        anObject = self._object
        if anObject is not None:
            for description in aDescription:
                self.useDuring(MAModel.readUsingWrapper(anObject, description), lambda: self.visit(description))

    def visitDescription(self, aDescription):
        self.validateUsing(self._object, aDescription)

