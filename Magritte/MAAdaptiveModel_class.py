
from MAContainer_class import MAContainer


class MAAdaptiveModel:

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
        return self.values[description] if description in self.values else None

    def writeUsing(self, description, value):
        self.values[description] = value

