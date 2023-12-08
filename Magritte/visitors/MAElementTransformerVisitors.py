from typing import Any

from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.descriptions.MADescription_class import MADescription
from descriptions.MAContainer_class import MAContainer
from descriptions.MAReferenceDescription_class import MAReferenceDescription


class MAElementTransformerVisitor(MAVisitor):
    """Abstract class defining common transformation interface based on MAElementDescription."""

    def visitReferenceDescription(self, description: MAReferenceDescription):
        raise TypeError(
            f"{self.__class__.__name__} cannot encode using reference description."
            " Only scalar values are allowed."
            )

    def visitContainer(self, description: MAContainer):
        raise TypeError(
            f"{self.__class__.__name__} cannot encode using container description."
            " Only scalar values are allowed."
            )


class MAWriterVisitor(MAElementTransformerVisitor):
    """Abstract class defining common interface for exporting/writing model
    to external value using MAElementDescription.
    """

    def write(self, model: Any, description: MADescription) -> Any:
        """Exports the model described by the description. Returns the exported value."""
        raise NotImplementedError(f"{self.__class__.__name__}.write() not implemented.")


class MAReaderVisitor(MAElementTransformerVisitor):
    """Abstract class defining common interface for importing/reading model
    from external value using MAElementDescription.
    """

    def read(self, src: Any, description: MADescription) -> Any:
        """Imports model described by the description from external value src. Returns the imported model."""
        raise NotImplementedError(f"{self.__class__.__name__}.read() not implemented.")
