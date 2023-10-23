from typing import Any

from MABooleanDescription_class import MABooleanDescription
from MAStringDescription_class import MAStringDescription
from MAMagnitudeDescription_class import MAMagnitudeDescription
from MADescription_class import MADescription
from MAVisitor_class import MAVisitor


class MAInequalityFound(Exception):
    """Exception raised when inequality is found as early as possible."""
    pass


class MAEqualityTester(MAVisitor):
    """Compares to objects of the same type, using Magritte description."""

    def __init__(self):
        self._model1 = None
        self._model2 = None
        self._equal_nested = None

    def equal(self, model1: Any, model2: Any, description: MADescription) -> bool:
        self._equal_nested = []
        return self._test_for_equality(model1, model2, description)

    def _test_for_equality(self, model1: Any, model2: Any, description: MADescription) -> bool:
        self._model1 = model1
        self._model2 = model2
        try:
            self.visit(description)
        except MAInequalityFound:
            return False
        return True

    def _deeper(self, model1: Any, model2: Any, description: MADescription) -> bool:
        if model1 is None or model2 is None:
            if model1 is not model2:
                return False

        if isinstance(description, (MABooleanDescription, MAMagnitudeDescription, MAStringDescription)):
            if model1 != model2:
                return False

        if (model1, model2) in self._equal_nested:
            # protect from infinite recursion
            return True

        prev_model1 = self._model1
        prev_model2 = self._model2

        self._equal_nested.append((model1, model2))

        res = self._test_for_equality(model1, model2, description)

        if not res:
            self._equal_nested.remove((model1, model2))

        self._model1 = prev_model1
        self._model2 = prev_model2

        return res

    def visitElementDescription(self, description: MADescription):
        if description.accessor.read(self._model1) != description.accessor.read(self._model2):
            raise MAInequalityFound()

    def visitContainer(self, description: MADescription):
        self.visitAll(description)

    def visitReferenceDescription(self, description):
        ref_model1 = description.accessor.read(self._model1)
        ref_model2 = description.accessor.read(self._model2)
        if not self._deeper(ref_model1, ref_model2, description.reference):
            raise MAInequalityFound()

    def visitMultipleOptionDescription(self, description):  # MAMultipleOptionDescription is not implemented yet
        selected_options1 = description.accessor.read(self._model1)
        selected_options2 = description.accessor.read(self._model2)
        if selected_options1 is None or selected_options2 is None:
            if selected_options1 is not selected_options2:
                raise MAInequalityFound()

        for entry1 in selected_options1:
            res1 = False
            for entry2 in selected_options2:
                res1 |= self._deeper(entry1, entry2, description.reference)
            if not res1:
                raise MAInequalityFound()

    def visitToManyRelationDescription(self, description):
        collection1 = description.accessor.read(self._model1)
        collection2 = description.accessor.read(self._model2)
        if collection1 is None or collection2 is None:
            if collection1 is not collection2:
                raise MAInequalityFound()

        for entry1 in collection1:
            res1 = False
            for entry2 in collection2:
                res1 |= self._deeper(entry1, entry2, description.reference)
            if not res1:
                raise MAInequalityFound()
