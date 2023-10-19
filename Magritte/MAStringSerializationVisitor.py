from typing import Any
from datetime import timedelta, datetime

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
from MAContainer_class import MAContainer
from MATimeDescription_class import MATimeDescription


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
        if description.accessor.read(self._model) != description.undefinedValue:
            super().visit(description)
        else:
            raise TypeError(
                "MAStringSerializer cannot encode or decode undefined value."
        )
    
    def visitContainer(self, description: MAContainer):
        raise TypeError(
            "MAStringSerializer cannot encode or decode using container values description."
        )

    def visitDescription(self, description: MADescription):
        raise TypeError(
            "MAStringWriterVisitor cannot encode or decode using description."
        )


class MAStringWriterVisitor(MAStringVisitor):
    """Encodes the value described by the descriptions into string."""
    def __init__(self):
        self._str = None
    
    def visit(self, description: MADescription):
        if description.accessor.read(self._model) != description.undefinedValue:
            super().visit(description)
        else:
            self._str = description.undefined

    def write_str(self, model: Any, description: MADescription) -> str:
        self._model = model
        self.visit(description)
        return self._str

    def visitElementDescription(self, description: MAElementDescription):
        self._str = str(description.accessor.read(self._model))

    def visitBooleanDescription(self, description: MABooleanDescription):
        value = description.accessor.read(self._model)
        if type(value) == bool:
            self._str = str(value)
        elif type(value) in (tuple, list):
            self._str = str(description.accessor.read(self._model)[0])
        else:
            raise TypeError(
                "The boolean value cannot be serialized into a string"
            )
    
    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAStringWriterVisitor cannot encode using reference description."
        )


class MAStringReaderVisitor(MAStringVisitor):
    """Decodes the string into an appropriate value."""
    def __init__(self):
        self._val = None
    
    def visit(self, description: MADescription):
        if description.accessor.read(self._model) != description.undefined:
            super().visit(description)
        else:
            self._val = description.undefinedValue

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

    def visitTimeDescription(self, description: MATimeDescription):
        datetime_str = description.accessor.read(self._model)
        self._val = datetime.strptime(datetime_str, '%H:%M:%S').time()
    
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
    
    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            "MAStringReaderVisitor cannot encode using reference description."
        )
