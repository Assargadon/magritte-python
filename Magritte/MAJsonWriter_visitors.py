import json
from typing import Dict, Any, Union, List

from MABooleanDescription_class import MABooleanDescription
from MAStringDescription_class import MAStringDescription
from MAMagnitudeDescription_class import MAMagnitudeDescription
from MAContainer_class import MAContainer
from MADescription_class import MADescription
from MAReferenceDescription_class import MAReferenceDescription
from MAVisitor_class import MAVisitor


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


class MAObjectJsonWriter(MAVisitor):
    """Encodes the object described by the descriptions into JSON."""

    def __init__(self):
        self._model = None
        self._json = None
        self._value_encoder = MAValueJsonWriter()

    def _validate_name(self, description: MADescription) -> None:
        name = description.name
        if name is None:
            raise ValueError(
                f"MAObjectJsonWriter requires names for all the descriptions to construct valid Json. "
                f"Found None value for {description.label}."
                )
        if not isinstance(name, str):
            raise ValueError(
                f"MAObjectJsonWriter requires names for all the descriptions to be str to construct valid Json. "
                f"Found: {type(name)}."
                )
        if name in self._json:
            raise ValueError(
                f"MAObjectJsonWriter requires distinct names for all the descriptions to construct valid Json. "
                f"Found duplicate: {name}."
                )

    def write_json(self, model: Any, description: MADescription) -> Union[Dict, List, Any, None]:
        self._model = model
        self._json = None
        self.visit(description)
        return self._json

    def write_json_string(self, model: Any, description: MADescription) -> str:
        return json.dumps(self.write_json(model, description))

    def _deeper(self, model: Any, description: MADescription) -> Union[Dict, List, Any, None]:
        if model is None:
            return None
        # if isinstance(model, (int, float, str, bool, datetime)):
        # Better to check the type of the description, not the model, since the model can be an object but accessor can
        # return a scalar value.
        if isinstance(description, (MABooleanDescription, MAMagnitudeDescription, MAStringDescription)):
            return self._value_encoder.write_json(model, description)

        prev_json = self._json
        prev_model = self._model

        res = self.write_json(model, description)

        self._json = prev_json
        self._model = prev_model

        return res

    def visit(self, description: MADescription):
        if self._model == description.undefinedValue:
            return
        if not description.visible:
            return
        super().visit(description)

    def visitElementDescription(self, description: MADescription):
        self._validate_name(description)
        self._json[description.name] = self._value_encoder.write_json(self._model, description)

    def visitContainer(self, description: MADescription):
        if not self._json:
            self._json = {}
            self.visitAll(description)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self.json")

    def visitReferenceDescription(self, description):
        self._validate_name(description)
        model = description.accessor.read(self._model)
        if model is None:
            self._json[description.name] = None
        else:
            self._json[description.name] = self._deeper(model, description.reference)

    def visitMultipleOptionDescription(self, description):  # MAMultipleOptionDescription is not implemented yet
        self._validate_name(description)
        selected_options = description.accessor.read(self._model)
        if selected_options is None:
            self._json[description.name] = None
        else:
            self._json[description.name] = {self._deeper(entry, description.reference) for entry in selected_options}
        
    def visitToManyRelationDescription(self, description):
        self._validate_name(description)
        collection = description.accessor.read(self._model)
        self._json[description.name] = [
            self._deeper(entry, description.reference) for entry in collection
            ]
        
