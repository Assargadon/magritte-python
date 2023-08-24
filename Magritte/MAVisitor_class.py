
from MAValidationError_class import MAValidationError
from MAMultipleErrors_class import MAMultipleErrors


class MAVisitor:

    def visit(self, anObject):
        errors = []
        try:
            anObject.acceptMagritte(self)
        except MAValidationError as err:
            errors.append(err)
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
