
from copy import copy
from MADescription_class import MADescription
from MAIdentityAccessor_class import MAIdentityAccessor

class MAContainer(MADescription):

    @classmethod
    def isAbstract(cls):
        return False

    def __init__(self):
        super().__init__()
        self._children = self.defaultCollection()

    def __eq__(self, other):
        return super().__eq__(other) and self._children == other.children

    def __iadd__(self, anItem):
        self.append(anItem)

    def __contains__(self, item):
        return item in self._children

    def __len__(self):
        return len(self._children)

    def __getitem__(self, item):
        return self._children[item]

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.setChildren(copy(self.children))
        return clone


    @classmethod
    def defaultAccessor(cls):
        return MAIdentityAccessor()


    @property
    def children(self):
        return self._children

    def setChildren(self, aCollection):
        self._children = aCollection

    def isContainer(self):
        return True

    def notEmpty(self):
        return len(self.children) > 0

    def isEmpty(self):
        return len(self.children) == 0

    def hasChildren(self):
        return self.notEmpty()

    def append(self, aDescription):
        self.children.append(aDescription)

    def extend(self, aCollection):
        self.children.extend(aCollection)

    @classmethod
    def withDescription(cls, aDescription):
        result = cls()
        result.append(aDescription)
        return result

    @classmethod
    def withAllDescriptions(cls, aCollection):
        result = cls()
        result.extend(aCollection)
        return result

    @classmethod
    def defaultCollection(cls):
        return list()

    def asContainer(self):
        return self

    def get(self, index, default_value):
        return self.children[index] if index < len(self.children) else default_value


    def allSatisty(self, aBlock):
        return all(aBlock(item) for _, item in enumerate(self.children))

    def anySatisty(self, aBlock):
        return any(aBlock(item) for _, item in enumerate(self.children))

    def collect(self, aBlock):
        result = copy(self)
        items = [aBlock(item) for _, item in enumerate(self.children)]
        result.setChildren(items)
        return result

    def select(self, aBlock):
        result = copy(self)
        items = [item for _, item in enumerate(self.children) if aBlock(item)]
        result.setChildren(items)
        return result

    def reject(self, aBlock):
        result = copy(self)
        items = [item for _, item in enumerate(self.children) if not aBlock(item)]
        result.setChildren(items)
        return result


    def copyEmpty(self):
        result = copy(self)
        result.setChildren(self.defaultCollection())
        return result

    def copyRange(self, aStartIndex, anEndIndex):
        result = copy(self)
        items = self.children[aStartIndex:anEndIndex+1]
        result.setChildren(items)
        return result

    def copyWithout(self, anObject):
        return self.reject(lambda item: item == anObject)
        #result = copy(self)
        #items = [item for _, item in enumerate(self.children) if item != anObject]
        #result.setChildren(items)
        #return result

    def copyWithoutAll(self, aCollection):
        return self.reject(lambda item: item in aCollection)
        #result = copy(self)
        #items = [item for _, item in enumerate(self.children) if item not in aCollection]
        #result.setChildren(items)
        #return result


    def detect(self, aBlock):
        return next((item for item in self.children if aBlock(item)))

    def detectIfNone(self, aBlock, anExceptionBlock):
        return next((item for item in self.children if aBlock(item)), anExceptionBlock())

    def do(self, aBlock):
        for item in self.children: aBlock(item)

    def keysAndValuesDo(self, aBlock):
        for index, item in enumerate(self.children): aBlock(index, item)
