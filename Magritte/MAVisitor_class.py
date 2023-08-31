
from sys import intern
from errors.MAValidationError import MAValidationError
from errors.MAMultipleErrors import MAMultipleErrors


class MAValidationErrorContextManager():
    def __init__(self, anObject, onValidationError):
        self._obj = anObject
        self._hasOnValidationError = False
        self._savedOnValidationError = None
        self._newOnValidationError = onValidationError

    def __enter__(self):
        self._hasOnValidationError = hasattr(self._obj, intern('_onValidationError'))
        if self._hasOnValidationError:
            self._savedOnValidationError = self._obj._onValidationError
            self._obj._onValidationError = self._newOnValidationError

    def __exit__(self, type, value, traceback):
        if self._hasOnValidationError:
            self._obj._onValidationError = self._savedOnValidationError


class MAVisitor:

    def visit(self, anObject):
        errors = []
        def onValidationError(exc):
            errors.append(exc)
            return True

        with MAValidationErrorContextManager(anObject, onValidationError):
            anObject.acceptMagritte(self)

        if len(errors) > 0:
            multipleErrors = MAMultipleErrors(errors=errors, message=anObject.label)
            raise multipleErrors

    def visitAll(self, aCollection):
        for element in aCollection:
            self.visit(element)


    def visitDescription(self, anObject):
        pass

    def visitBlockDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitBooleanDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitClassDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitColorDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitContainer(self, anObject):
        self.visitDescription(anObject)

    def visitDirectoryDescription(self, anObject):
        self.visitFileDescription(anObject)

    def visitDateAndTimeDescription(self, anObject):
        self.visitMagnitudeDescription(anObject)

    def visitDurationDescription(self, anObject):
        self.visitMagnitudeDescription(anObject)

    def visitElementDescription(self, anObject):
        self.visitDescription(anObject)

    def visitFileDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitMagnitudeDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitMemoDescription(self, anObject):
        self.visitStringDescription(anObject)

    def visitMultipleOptionDescription(self, anObject):
        self.visitOptionDescription(anObject)

    def visitNumberDescription(self, anObject):
        self.visitMagnitudeDescription(anObject)

    def visitIntDescription(self, anObject):
        self.visitNumberDescription(anObject)

    def visitFloatDescription(self, anObject):
        self.visitNumberDescription(anObject)

    def visitOptionDescription(self, anObject):
        self.visitReferenceDescription(anObject)

    def visitPasswordDescription(self, anObject):
        self.visitStringDescription(anObject)

    def visitPriorityContainer(self, anObject):
        self.visitContainer(anObject)

    def visitReferenceDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitRelationDescription(self, anObject):
        self.visitReferenceDescription(anObject)

    def visitReportContainer(self, anObject):
        self.visitContainer(anObject)

    def visitSingleOptionDescription(self, anObject):
        self.visitOptionDescription(anObject)

    def visitStringDescription(self, anObject):
        self.visitElementDescription(anObject)

    def visitSymbolDescription(self, anObject):
        self.visitStringDescription(anObject)

    def visitTableDescription(self, anObject):
        self.visitReferenceDescription(anObject)

    def visitTableReference(self, anObject):
        self.visitReferenceDescription(anObject)

    def visitTimeDescription(self, anObject):
        self.visitMagnitudeDescription(anObject)

    def visitTimeStampDescription(self, anObject):
        self.visitMagnitudeDescription(anObject)

    def visitToManyRelationDescription(self, anObject):
        self.visitRelationDescription(anObject)

    def visitToManyScalarRelationDescription(self, anObject):
        self.visitToManyRelationDescription(anObject)

    def visitToOneRelationDescription(self, anObject):
        self.visitRelationDescription(anObject)

    def visitTokenDescription(self, anObject):
        self.visitReferenceDescription(anObject)

    def visitUrlDescription(self, aMAUrlDescription):
        self.visitElementDescription(aMAUrlDescription)
