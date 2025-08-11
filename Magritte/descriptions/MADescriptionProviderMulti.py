
from abc import abstractmethod
from Magritte.descriptions.MADescription_class import MADescription


class MADescriptionProviderMulti:

    def __init__(self):
        self._all_descriptions = list()
        self._descriptions_by_model_name = dict()
        self.instatiate_descriptions()

    def register_description(self, aDescription: MADescription):
        """
            Should be called inside instatiate_descriptions only.
            Should be called only after a name is assigned to a description.
        """
        model_name = aDescription.name
        if model_name is None:
            raise TypeError('register_description should be called only after a name is assigned to a description')
        if model_name in self._descriptions_by_model_name:
            return
        self._descriptions_by_model_name[model_name] = aDescription
        self._all_descriptions.append(aDescription)

    @abstractmethod
    def instatiate_descriptions(self):
        """Method to generate the descriptions."""
        pass

    @property
    def all_descriptions(self) -> list[MADescription]:
        """Returns all descriptions."""
        return self._all_descriptions

    def description_for(self, model_name: str) -> MADescription:
        """Returns a model description for the given model type."""
        if model_name in self._descriptions_by_model_name:
            return self._descriptions_by_model_name[model_name]
        raise ValueError(f'Unknown model type: {model_name}')
