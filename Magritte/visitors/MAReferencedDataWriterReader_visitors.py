
from typing import Any, Union
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.MAModel_class import MAModel


class MAReferencedDataUntangler(MAVisitor):

    class _Context:
        model: Any = None
        description: MADescription = None
        value_index: int = None
        subcontexts: list = None

    #class _Reference:
    #    value: Any = None
    #    reference_index: int = 0

    def __init__(self):
        self._clear()

    def _clear(self):
        self._raw_index = 0
        self._values_by_index = {}
        self._values_by_identifier = {}
        self._contexts = []
        self._contexts_by_index = {}
        self._createEmptyContext()

    def result(self):
        values = self._values_by_index
        tree = self._contexts[0]
        return { 'values': values, 'tree': tree }

    def _createEmptyContext(self):
        self._context = self.__class__._Context()
        self._contexts.append(self._context)
        return self._context

    #def _pushContext(self):
    #    self._contexts.append(self._context)

    #def _popContext(self):
    #    self._context = self._contexts.pop()

    def _addValue(self, aValue):
        value_index = self._raw_index
        self._raw_index += 1
        self._values_by_index[value_index] = aValue
        return value_index

    def _addValueWithCheck(self, aValue):
        identifier = id(aValue)
        if identifier in self._values_by_identifier:
            was_added = False
            reference_index = self._values_by_identifier[identifier].reference_index
        else:
            was_added = True
            reference_index = self._raw_index
            self._raw_index += 1
            #reference = self.__class__._Reference()
            #reference.reference_index = reference_index
            #reference.value = aValue
            self._values_by_identifier[identifier] = aValue
            self._values_by_index[reference_index] = aValue
        return (reference_index, was_added,)

    def _walkModel(self, aModel: Any, aDescription: MADescription):
        self._clear()
        self._context.model = aModel
        self._context.description = aDescription
        self._walkFromCurrent()

    def _walkFromCurrent(self):
        model = self._context.model
        description = self._context.description
        if model == description.undefinedValue:
            return
        if not description.visible:
            return
        description.acceptMagritte(self)

    def visitElementDescription(self, description: MADescription):
        context = self._context
        model = context.model
        value = MAModel.readUsingWrapper(model, description)
        value_index = self._addValue(value)
        context.value_index = value_index

    def visitContainer(self, description: MAContainer):
        context = self._context
        model = context.model
        context.subcontexts = []
        for subdescription in description:
            submodel = MAModel.readUsingWrapper(model, subdescription)
            subcontext = self._createEmptyContext()
            context.subcontexts.append(subcontext)
            subcontext.model = submodel
            subcontext.description = subdescription.reference
            self._walkFromCurrent()

    def visitToOneRelationDescription(self, description: MAReferenceDescription):
        context = self._context
        model = context.model
        value = MAModel.readUsingWrapper(model, description)
        (reference_index, was_added,) = self._addValueWithCheck(value)
        if was_added:
            subcontext = self._createEmptyContext()
            subcontext.model = value
            subcontext.description = description.reference
            self._contexts_by_index = reference_index
            self._walkFromCurrent()
        else:
            subcontext = self._contexts_by_index[reference_index]
        context.subcontexts = [subcontext]

    def visitToManyRelationDescription(self, description):
        context = self._context
        model = context.model
        values = MAModel.readUsingWrapper(model, description)
        context.subcontexts = []
        for value in values:
            (reference_index, was_added,) = self._addValueWithCheck(value)
            if was_added:
                subcontext = self._createEmptyContext()
                subcontext.model = value
                subcontext.description = description.reference
                self._contexts_by_index = reference_index
                self._walkFromCurrent()
            else:
                subcontext = self._contexts_by_index[reference_index]
            context.subcontexts.append(subcontext)

