import json
from typing import Dict, Any

from MAVisitor_class import MAVisitor
from MAContainer_class import MAContainer
from MADescription_class import MADescription
from MAReferenceDescription_class import MAReferenceDescription

class MAValueJsonWriter(MAVisitor):
    """Encodes the value described by the descriptions into JSON."""

    def __init__(self, description: MADescription):
        if description.isContainer():
            raise TypeError(
                "MAValueJsonWriter cannot encode using container description. Only scalar values are allowed. Use MAObjectJsonWriter instead."
            )
        self._description = description
        self._model = None
        self._json = None

    def write_json(self, model) -> Any:
        self._model = model
        self._json = self._description.undefinedValue
        self.visit(self._description)
        return self._json

    def write_json_string(self, model) -> str:
        return json.dumps(self.write_json(model))

    def visit(self, description: MADescription):
        if description.accessor.canRead(self._model):
            super().visit(description)
        else:
            raise ValueError("MAValueJsonWriter failed to read value from the model using the description provided.")

    def visitElementDescription(self, description: MADescription):
        self._json = description.accessor.read(self._model)

    def visitDateAndTimeDescription(self, description: MADescription):
        self._json = description.accessor.read(self._model).isoformat()

    def visitMagnitudeDescription(self, description: MADescription):
        # !TODO Override exact visit methods like visitDateAndTimeDescription for each type of magnitude when they are defined.
        self._json = description.accessor.read(self._model)

    def visitReferenceDescription(self, description: MAReferenceDescription):
        if description.reference.isContainer():
            # referenced value is an object
            nested_encoder = MAObjectJsonWriter(description.reference)
        else:
            # referenced value is a scalar value
            nested_encoder = MAValueJsonWriter(description.reference)
        self._json = nested_encoder.write_json(description.accessor.read(self._model))



class MAObjectJsonWriter(MAVisitor):
    """Encodes the object described by the descriptions into JSON."""

    def __init__(self, description: MAContainer):
        if not description.isContainer():
            raise TypeError(
                "MAObjectJsonWriter cannot encode using scalar description. Only container values are allowed. Use MAValueJsonWriter instead."
            )
        self._description = description
        self._model = None
        self._json = None

    def write_json(self, model) -> Dict[str, Any]:
        self._model = model
        self._json = {}  # Reset the json dict.
        for elementDescription in self._description:
            self.visit(elementDescription)
        return self._json

    def write_json_string(self, model) -> str:
        return json.dumps(self.write_json(model))

    def visitElementDescription(self, description: MADescription):
        value_encoder = MAValueJsonWriter(description)
        name = description.name
        if name is None:
            raise ValueError("MAObjectJsonWriter requires names for all the descriptions to construct valid Json. Found None value.")
        if not isinstance(name, str):
            raise ValueError(f"MAObjectJsonWriter requires names for all the descriptions to be str to construct valid Json. Found: {type(name)}")
        if name in self._json:
            raise ValueError(f"MAObjectJsonWriter requires distinct names for all the descriptions to construct valid Json. Found duplicate: {name}.")
        self._json[name] = value_encoder.write_json(self._model)

