
import json
from typing import Any
from datetime import datetime

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor

class MAValueJsonReader(MAVisitor):
    """Decodes the value described by the description from JSON and writes to model."""

    def __init__(self):
        self._model = None
        self._value = None

    def read_json(self, model: Any, description: MADescription, value: Any):
        self._model = model
        self._value = value
        self.visit(description)

    def read_json_string(self, model: Any, description: MADescription, value_str: str):
        value = json.loads(value_str)
        self.read_json(model, description, value)

    def visitElementDescription(self, description: MADescription):
        description.accessor.write(self._model, self._value)

    def visitDateAndTimeDescription(self, description: MADescription):
        dateTimeValue = datetime.fromisoformat(self._value)
        description.accessor.write(self._model, dateTimeValue)

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAValueJsonReader cannot encode using reference description."
            " Only scalar values are allowed. "
            )

    def visitContainer(self, description: MAContainer):
        raise TypeError(
            "MAValueJsonReader cannot decode using container description."
            " Only scalar values are allowed. "
            )

