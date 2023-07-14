
from MADescription_class import MADescription
from MAIdentityAccessor_class import MAIdentityAccessor

class MAContainer(MADescription):

    @classmethod
    def isAbstract(cls):
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._children = self.defaultCollection()

    def __eq__(self, other):
        return self._children == other.children

    def __iadd__(self, anItem):
        self._children += anItem

    def __contains__(self, item):
        return item in self._children

    def __len__(self):
        return len(self._children)

    def __getitem__(self, item):
        return self._children[item]


    @classmethod
    def defaultAccessor(cls):
        return MAIdentityAccessor()


    @property
    def children(self):
        return self._children

    def isContainer(self):
        return True

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

