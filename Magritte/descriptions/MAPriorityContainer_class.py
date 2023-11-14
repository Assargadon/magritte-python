
from bisect import insort
from copy import copy

from Magritte.descriptions.MAContainer_class import MAContainer


class MAPriorityContainer(MAContainer):

    def append(self, aDescription):
        insort(self.children, aDescription)

    def extend(self, aCollection):
        for item in aCollection:
            self.append(item)

    def resort(self):
        self.setChildren(copy(self.children))

    def setChildren(self, aCollection):
        super().setChildren(sorted(aCollection))


    def acceptMagritte(self, aVisitor):
        aVisitor.visitPriorityContainer(self)
