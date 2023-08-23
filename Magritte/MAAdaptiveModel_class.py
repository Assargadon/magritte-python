
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

    def readUsing(self, aDescription):
        return self.values[aDescription] if aDescription in self.values else None

    def writeUsing(self, anObject, aDescription):
        self.values[aDescription] = anObject

