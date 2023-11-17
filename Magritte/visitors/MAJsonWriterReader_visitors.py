import json
from typing import Dict, Any, Union, List
from datetime import timedelta, datetime
import logging
import sys

#logging.basicConfig(level=logging.DEBUG)
#sys.stdout = open('output.txt', 'w')

from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.visitors.MAStringWriterReader_visitors import parse_timedelta

from Magritte.visitors.MAVisitor_class import MAVisitor


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
        

class MAValueJsonReader(MAVisitor):
    """
    Decodes the JSON value into an atribute of an 
    object described by the descriptions.
    """

    def __init__(self):
        self._model = None
        self._attr_value = None

    def visit(self, description: MADescription):
        if self._model != description.undefinedValue:
            super().visit(description)
        else:
            self._val = description.undefinedValue

    def read_json(self, json_val: Any, description: MADescription) -> Any:
        self._model = json_val
        self.visit(description)
        return self._attr_value

    def visitElementDescription(self, description: MADescription):
        self._attr_value = description.accessor.read(self._model)

    def visitDateAndTimeDescription(self, description: MADateAndTimeDescription):
        try:
            self._attr_value = datetime.strptime(self._model, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self._attr_value = datetime.strptime(self._model, '%Y-%m-%d %H:%M:%S.%f')

    def visitDateDescription(self, description: MADateDescription):
        self._attr_value = datetime.strptime(self._model, '%Y-%m-%d').date()

    def visitTimeDescription(self, description: MATimeDescription):
        try:
            self._attr_value = datetime.strptime(self._model, '%H:%M:%S').time()
        except ValueError:
            self._attr_value = datetime.strptime(self._model, '%H:%M:%S.%f')
    
    def visitDurationDescription(self, description: MADurationDescription):
        self._attr_value = parse_timedelta(self._model)

    def visitBooleanDescription(self, description: MABooleanDescription):
        bool_str = description.accessor.read(self._model).lower()
        self._attr_value = bool_str

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAValueJsonReader cannot encode using reference description."
            " Only scalar values are allowed. Use MAObjectJsonReader instead."
        )

    def visitContainer(self, description: MAContainer):
        raise TypeError(
            "MAValueJsonReader cannot encode using container description."
            " Only scalar values are allowed. Use MAObjectJsonReader instead."
        )


class ResponseObject:
    pass


class MAObjectJsonReader(MAVisitor):
    """Decodes the JSON into an object described by descriptions."""
    def __init__(self):
        self._model = None
        self._obj = None
        self._value_decoder = MAValueJsonReader()
    
    def _validate_name(self, description: MADescription) -> None:
        name = description.name
        if name is None:
            raise ValueError(
                f"MAObjectJsonReader requires names for all the descriptions to construct valid model. "
                f"Found None value for {description.label}."
            )

        if not isinstance(name, str):
            raise ValueError(
                f"MAObjectJsonReader requires names for all the descriptions to be str to construct valid model. "
                f"Found: {type(name)}."
            )

        if self._obj and name in self._obj.__dir__():
            raise ValueError(
                f"MAObjectJsonReader requires distinct names for all the descriptions to construct valid model. "
                f"Found duplicate: {name}."
            )
    
    @staticmethod
    def _json_loader(src: str) -> Any:
        try:
            return json.loads(src)
        except (ValueError, TypeError) as e:
            raise TypeError

    def read_json(self, json_obj: str, description: MADescription) -> Any:
        self._model = self._json_loader(json_obj)
        self._obj = None
        self.visit(description)
        return self._obj

    def visit(self, description: MADescription):
        if self._model == description.undefined:
            return
        if not description.visible:
            return
        super().visit(description)

    def visitElementDescription(self, description: MADescription):
        self._validate_name(description)
        if not self._obj:
            self._obj = ResponseObject()
        setattr(self._obj, description.name, self._value_decoder.read_json(self._model, description))
    
    def _deeper(self, model: Any, description: MADescription) -> ResponseObject:
        if model is None:
            return None

        if isinstance(description, (MABooleanDescription, MAMagnitudeDescription, MAStringDescription)):
            return self._value_decoder.read_json(model, description)

        prev_obj = self._obj
        prev_model = self._model

        res = self.read_json(json.dumps(model), description)

        self._obj = prev_obj
        self._model = prev_model

        return res
    
    def visitContainer(self, description: MADescription):
        if not self._obj:
            self._obj = ResponseObject()
            for elem in zip(self._model.items(), description):
                key = elem[0][0]
                value = elem[0][1]
                description = elem[1]
                if isinstance(
                    description, (MAStringDescription, MAIntDescription, MAFloatDescription)
                ):
                    setattr(self._obj, key, value)
                elif isinstance (
                    description, (MAReferenceDescription, MAToOneRelationDescription)
                ):
                    self.visit(description=description)
                else:
                    attr_value = self._value_decoder.read_json(json_val=str(value), description=description)
                    setattr(self._obj, key, attr_value)
        else:
            raise Exception("Shouldn't reach visitContainer with nonempty self._obj")

    def visitReferenceDescription(self, description):
        self._validate_name(description)
        if not self._obj:
            self._obj = ResponseObject()
        try:
            ref_model = self._model["ref_object"]
        except KeyError:
            ref_model = None

        if ref_model is None:
            setattr(self._obj, description.name, None)
        else:
            setattr(self._obj, description.name, self._deeper(ref_model, description.reference))

    def visitToManyRelationDescription(self, description):
        self._validate_name(description)
        if not self._obj:
            self._obj = ResponseObject()
        try:
            collection = self._model["ref_objects"]
        except KeyError:
            collection = None

        if collection is None:
            setattr(self._obj, description.name, None)
        setattr(self._obj, description.name, [])
        for entry in collection:
            getattr(self._obj, description.name).append(self._deeper(entry, description.reference))
