import json
from typing import Dict, Any, Union, List

from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from descriptions.MAContainer_class import MAContainer
from descriptions.MADescription_class import MADescription
from descriptions.MAReferenceDescription_class import MAReferenceDescription

from visitors.MAVisitor_class import MAVisitor


class MAValueJsonWriter(MAVisitor):
    """Encodes the value described by the descriptions into JSON."""

    def __init__(self):
        self._model = None
        self._json = None

    @staticmethod
    def _test_jsonable(src: Any) -> Any:
        try:
            json.dumps(src)
        except (ValueError, TypeError):
            # just re-raise the exception
            raise
        else:
            return src

    def write_json(self, model: Any, description: MADescription) -> Any:
        self._model = model
        self._json = self._test_jsonable(description.undefinedValue)
        self.visit(description)
        return self._json

    def write_json_string(self, model: Any, description: MADescription) -> str:
        return json.dumps(self.write_json(model, description))

    def visit(self, description: MADescription):
        if self._model != description.undefinedValue:
            super().visit(description)

    def visitElementDescription(self, description: MADescription):
        self._json = self._test_jsonable(description.accessor.read(self._model))

    def visitDateAndTimeDescription(self, description: MADescription):
        value = description.accessor.read(self._model)
        self._json = self._test_jsonable(value.isoformat() if value else None)

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAValueJsonWriter cannot encode using reference description."
            " Only scalar values are allowed. Use MAObjectJsonWriter instead."
            )

    def visitContainer(self, description: MAContainer):
        raise TypeError(
            "MAValueJsonWriter cannot encode using container description."
            " Only scalar values are allowed. Use MAObjectJsonWriter instead."
            )


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
        if not description.visible: return

        value_encoder = MAValueJsonWriter(description)
        name = description.name
        if name is None:
            raise ValueError(f"MAObjectJsonWriter requires names for all the descriptions to construct valid Json. Found None value for {description.label}")
        if not isinstance(name, str):
            raise ValueError(f"MAObjectJsonWriter requires names for all the descriptions to be str to construct valid Json. Found: {type(name)}")
        if name in self._json:
            raise ValueError(f"MAObjectJsonWriter requires distinct names for all the descriptions to construct valid Json. Found duplicate: {name}.")
        self._json[name] = value_encoder.write_json(self._model)
        

    def visitToManyRelationDescription(self, description):
        if not description.visible: return

        name = description.name
        if name is None:
            raise ValueError(f"MAObjectJsonWriter requires names for all the descriptions to construct valid Json. Found None value for {description.label}")
        if not isinstance(name, str):
            raise ValueError(f"MAObjectJsonWriter requires names for all the descriptions to be str to construct valid Json. Found: {type(name)}")
        if name in self._json:
            raise ValueError(f"MAObjectJsonWriter requires distinct names for all the descriptions to construct valid Json. Found duplicate: {name}.")

        object_encoder = MAObjectJsonWriter(description.reference)
        collection = description.accessor.read(self._model) # TODO: replace on model.readUsing or description.read (both are not implemented yet)
        self._json[name] = [object_encoder.write_json(entry) for entry in collection]    
