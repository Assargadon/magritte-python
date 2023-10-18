from typing import Dict, Any, Union, List
from datetime import timedelta, datetime
from loguru import logger

from MAVisitor_class import MAVisitor
from MADescription_class import MADescription
from MAReferenceDescription_class import MAReferenceDescription
from MAElementDescription_class import MAElementDescription
from MAIntDescription_class import MAIntDescription
from MABooleanDescription_class import MABooleanDescription
from MAFloatDescription_class import MAFloatDescription
from MADateDescription_class import MADateDescription
from MADurationDescription_class import MADurationDescription
from MADateAndTimeDescription_class import MADateAndTimeDescription


def parse_timedelta(duration_str):
    parts = duration_str.split(', ')

    days = seconds = minutes = hours = 0

    for part in parts:
        if 'day' in part:
            days = int(part.split()[0])
        elif ':' in part:
            time_parts = part.split(':')
            if len(time_parts) == 2:
                hours, minutes = map(int, time_parts)
            elif len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)
                
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)



class MAStringVisitor(MAVisitor):
    def __init__(self):
        self._model = None

    def visit(self, description: MADescription):
        if self._model != description.undefinedValue:
            super().visit(description)

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAStringWriterVisitor cannot encode using reference description."
        )


class MAStringWriterVisitor(MAStringVisitor):
    """Encodes the value described by the descriptions into string."""
    def __init__(self):
        self._str = None

    def write_str(self, model: Any, description: MADescription) -> str:
        self._model = model
        self.visit(description)
        return self._str

    def visitElementDescription(self, description: MAElementDescription):
        self._str = str(description.accessor.read(self._model))

    def visitBooleanDescription(self, description: MABooleanDescription):
        if type(description.accessor.read(self._model)) == bool:
            self._str = str(description.accessor.read(self._model))
        elif type(description.accessor.read(self._model)) in (tuple, list):
            self._str = str(description.accessor.read(self._model)[0])
        else:
            raise TypeError(
                "The bollean value cannot be serialized into a string"
            )


class MAStringReaderVisitor(MAStringVisitor):
    """Decodes the string into an appropriate value."""
    def __init__(self):
        self._val = None

    def read_str(self, model: Any, description: MADescription):
        self._model = model
        self.visit(description)
        return self._val

    def visitElementDescription(self, description: MAElementDescription):
        self._val = description.accessor.read(self._model)

    def visitIntDescription(self, description: MAIntDescription):
        self._val = int(description.accessor.read(self._model))

    def visitFloatDescription(self, description: MAFloatDescription):
        self._val = float(description.accessor.read(self._model))

    def visitDateAndTimeDescription(self, description: MADateAndTimeDescription):
        datetime_str = description.accessor.read(self._model)
        self._val = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    def visitDateDescription(self, description: MADateDescription):
        datetime_str = description.accessor.read(self._model)
        self._val = datetime.strptime(datetime_str, '%Y-%m-%d').date()
    
    def visitDurationDescription(self, description: MADurationDescription):
        date_time_str = description.accessor.read(self._model)
        self._val = parse_timedelta(date_time_str)

    def visitBooleanDescription(self, description: MABooleanDescription):
        value = description.accessor.read(self._model)
        if type(value) == str:
            bool_str = description.accessor.read(self._model).lower()
        elif type(value) in (tuple, list):
            bool_str = value[0].lower()

        if bool_str in description.defaultTrueStrings():
            self._val = True
        elif bool_str in description.defaultFalseStrings():
            self._val = False
        else:
            raise TypeError(
                "The string cannot be deserialized into a boolean value"
            )
