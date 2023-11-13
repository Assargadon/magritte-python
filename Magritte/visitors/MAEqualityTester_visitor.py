from typing import Any
import logging

from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from descriptions.MADescription_class import MADescription
from visitors.MAVisitor_class import MAVisitor

logger = logging.getLogger(__name__)


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

    def _validate(self, model: Any, description: MADescription) -> bool:
        validation_errors = description.validate(model)
        if len(validation_errors) > 0:
            logger.error(
                f"Model {model!r} is not valid for description {description}. "
                f"Errors: {validation_errors}."
                )
            raise ValueError(
                f"Model {model!r} is not valid for description {description}. "
                f"Errors: {validation_errors}."
                )

    def _test_for_equality(self, model1: Any, model2: Any, description: MADescription) -> bool:
        self._validate(model1, description)
        self._validate(model2, description)
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

    def visit(self, description: MADescription):
        if self._model1 is None or self._model2 is None:
            if self._model1 is not self._model2:
                raise MAInequalityFound()
            return  # both models are None
        super().visit(description)  # both models are not None

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
