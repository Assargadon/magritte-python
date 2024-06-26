
from Magritte.MAModel_class import MAModel
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.errors.MAReadError import MAReadError
from Magritte.errors.MAWriteError import MAWriteError


class MAAdaptiveModel(MAModel):

    def __init__(self):
        self.magritteDescription = self.defaultDescription()
        self.values = self.defaultDictionary()

    @classmethod
    def defaultDescription(cls):
        return MAContainer()

    @classmethod
    def defaultDictionary(cls):
        return dict()

    def readUsing(self, description):
        if description not in self.magritteDescription:
            raise MAReadError()
        return self.values[description] if description in self.values else None

    def writeUsing(self, description, value):
        if description not in self.magritteDescription:
            raise MAWriteError()
        self.values[description] = value