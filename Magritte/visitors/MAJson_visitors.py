import json
from datetime import timezone
from typing import Dict, Any, Union, List

from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription

from Magritte.visitors.MAVisitor_class import MAVisitor


class MAValueJsonWriter(MAVisitor):
    """Encodes the value described by the descriptions into JSON."""

    def __init__(self):
        self._model = None
        self._accessor = None
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

    def write_json(self, model: Any, description: MADescription, accessor=None) -> Any:
        self._model = model
        self._accessor = description.accessor if accessor is None else accessor
        self._json = self._test_jsonable(description.undefinedValue)
        self.visit(description)
        return self._json

    def write_json_string(self, model: Any, description: MADescription) -> str:
        return json.dumps(self.write_json(model, description))

    def visit(self, description: MADescription):
        if self._model != description.undefinedValue:
            super().visit(description)

    def visitElementDescription(self, description: MADescription):
        value_jsonable = self._accessor.read(self._model)
        self._json = self._test_jsonable(value_jsonable)

    def visitDateAndTimeDescription(self, description: MADescription):
        value = self._accessor.read(self._model)
        value_jsonable = value.astimezone(timezone.utc).isoformat() if value else None
        self._json = self._test_jsonable(value_jsonable)

    def visitDateDescription(self, description: MADescription):
        value = self._accessor.read(self._model)
        value_jsonable = value.strftime('%Y-%m-%d') if value else None
        self._json = self._test_jsonable(value_jsonable)

    def visitTimeDescription(self, description: MADescription):
        value = self._accessor.read(self._model)
        value_jsonable = value.strftime('%H:%M:%S')
        self._json = self._test_jsonable(value_jsonable)

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


class MAValueJsonReader(MAVisitor):
    """Decodes a JSON value into the true value described by the MADescription."""

    def __init__(self):
        self._model = None
        self._json_value = None
        self._decoded_value = None

    def read_json(self, model: Any, json_value: Any, description: MADescription) -> Any:
        self._model = model
        self._json_value = json_value
        self._decoded_value = None
        self.visit(description)
        return self._decoded_value

    def _write_to_model(self, description: MADescription):
        if self._model is not None:
            description.accessor.write(self._model, self._decoded_value)

    def visit(self, description: MADescription):
        if self._json_value != description.undefinedValue:
            super().visit(description)

    def visitElementDescription(self, description: MADescription):
        self._decoded_value = self._json_value
        self._write_to_model(description)

    def visitDateAndTimeDescription(self, description: MADescription):
        from datetime import datetime
        if self._json_value is None:
            self._decoded_value = description.undefinedValue
        else:
            if self._json_value[-1] in ('Z', 'z'):
                self._json_value = self._json_value[:-1] + '+00:00'
            self._decoded_value = datetime.fromisoformat(self._json_value)
        self._write_to_model(description)

    def visitDateDescription(self, description: MADescription):
        from datetime import datetime
        if self._json_value is None:
            self._decoded_value = description.undefinedValue
        else:
            self._decoded_value = datetime.strptime(self._json_value, "%Y-%m-%d").date()
        self._write_to_model(description)

    def visitTimeDescription(self, description: MADescription):
        from datetime import datetime
        if self._json_value is None:
            self._decoded_value = description.undefinedValue
        else:
            self._decoded_value = datetime.strptime(self._json_value, "%H:%M:%S").time()
        self._write_to_model(description)

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAValueJsonReader cannot decode using reference description."
            "Only scalar values are allowed."
            )

    def visitContainer(self, description: MAContainer):
        raise TypeError(
            "MAValueJsonReader cannot decode using container description."
            "Only scalar values are allowed."
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
        if self._json and name in self._json:
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
        if not self._json:
            self._json = {}
        self._json[description.name] = self._value_encoder.write_json(self._model, description)

    def visitContainer(self, description: MADescription):
        if not self._json:
            self._json = {}
            self.visitAll(description)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self._json")

    def visitReferenceDescription(self, description):
        self._validate_name(description)
        if not self._json:
            self._json = {}
        ref_model = description.accessor.read(self._model)
        if ref_model is None:
            self._json[description.name] = None
        else:
            self._json[description.name] = self._deeper(ref_model, description.reference)

    def visitMultipleOptionDescription(self, description):  # MAMultipleOptionDescription is not implemented yet
        self._validate_name(description)
        if not self._json:
            self._json = {}
        selected_options = description.accessor.read(self._model)
        if selected_options is None:
            self._json[description.name] = None
        else:
            self._json[description.name] = {
                self._deeper(entry, description.reference) for entry in selected_options
                }
        
    def visitToManyRelationDescription(self, description):
        self._validate_name(description)
        if not self._json:
            self._json = {}
        collection = description.accessor.read(self._model)
        if collection is None:
            self._json[description.name] = None
        self._json[description.name] = [
            self._deeper(entry, description.reference) for entry in collection
            ]
        
