
from Magritte.descriptions.MADescription_class import MADescription

class MADescriptionProvider:
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self._all_descriptions = list()
        self._descriptions_by_model_type = dict()
        self.instatiate_descriptions()

    def register_description(self, aDescription: MADescription):
        """Should be called inside register_description only."""
        model_type = aDescription.name
        if model_type in self._descriptions_by_model_type:
            return
        self._descriptions_by_model_type[model_type] = aDescription
        self._all_descriptions.append(aDescription)

    def instatiate_descriptions(self):
        """Method to generate the descriptions."""
        raise TypeError('Abstract method, must be overridden')

    @property
    def all_descriptions(self) -> list[MADescription]:
        """Returns all descriptions."""
        return self._all_descriptions

    def description_for(self, model_type: str) -> MADescription:
        """Returns a model description for the given model type."""
        if model_type in self._descriptions_by_model_type:
            return self._descriptions_by_model_type[model_type]
        raise ValueError(f'Unknown model type: {model_type}')
