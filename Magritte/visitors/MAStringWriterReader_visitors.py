from typing import Any, Union
from datetime import timedelta, datetime

from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MATimeDescription_class import MATimeDescription


def parse_timedelta(duration_str: str) -> timedelta:
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


def is_bool_tuple(val: Union[bool, tuple], description: MADescription) -> bool:
    """
    Bool accessor returns True for true value and (False, ) for False value,
    so we will check both cases for now until we refactor
    """
    if type(val) == tuple:
        return type(val[0]) == bool
    return type(val) in (description.defaultKind(), tuple)


class MAStringVisitor(MAVisitor):
    def __init__(self):
        self._model = None
    
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
            val = description.accessor.read(self._model)
            if is_bool_tuple(val=val, description=description):
                super().visit(description)
            else:
                raise TypeError(
                    "Wrong value type"
                )
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

        try:
            self._str = str(value)
        except TypeError as e:
            raise TypeError(
                "The boolean value cannot be serialized into a string")

    
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
        if datetime_str[-1] in ('Z', 'z'):
            datetime_str = datetime_str[:-1] + '+00:00'
        self._val = datetime.fromisoformat(datetime_str)

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
        bool_str = description.accessor.read(self._model).lower()


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
