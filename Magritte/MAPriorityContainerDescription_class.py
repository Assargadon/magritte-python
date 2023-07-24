
from bisect import insort
from copy import copy
from MAContainer_class import MAContainer

class MAPriorityContainerDescription(MAContainer):

    def append(self, aDescription):
        insort(self.children, aDescription)

    def extend(self, aCollection):
        for item in aCollection:
            self.append(item)

    def moveDown(self, aDescription):
        raise NotImplementedError()

    def moveUp(self, aDescription):
        raise NotImplementedError()

    def resort(self):
        self.setChildren(copy(self.children))

    def setChildren(self, aCollection):
        super().setChildren(aCollection.sort())

