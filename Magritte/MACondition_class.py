

class MACondition:

    @classmethod
    def isAbstract(cls):
        return cls == MACondition

    @classmethod
    def receiverSelector(cls, anObject, aSelector):
        cls.receiverSelectorArgumentsIndex(anObject, aSelector, [None], 1)

    @classmethod
    def receiverSelectorArgumentsIndex(cls, anObject, aSelector, anArgumentsArray, anIndex):
        if len(anArgumentsArray) > 0 and anIndex not in range(0, len(anArgumentsArray)):
            raise Exception('Index out of bounds.')
        c = MAPluggableCondition(anObject, aSelector, anArgumentsArray, anIndex)
        return c

    @classmethod
    def selector(cls, aSelector):
        return cls.receiverSelectorArgumentsIndex(None, aSelector, [], 0)

    @classmethod
    def selectorArgument(cls, aSelector, anObject):
        return cls.receiverSelectorArgumentsIndex(None, aSelector, [anObject], 0)

    def numArgs(self):
        return 1

    def value(self, anObject):
        pass



class MAPluggableCondition(MACondition):

    def __init__(self, anObject, aSelector, anArgumentsArray, anIndex):
        self.receiver = anObject
        self.selector = aSelector
        self.arguments = anArgumentsArray
        self.index = anIndex

    def value(self, anObject):
        actualReceiver = anObject if self.index == 0 else self.receiver
        if self.index > 0:
            actualArguments = self.arguments.copy()
            actualArguments[self.index] = anObject
        else:
            actualArguments = self.arguments
        selectorMethod = actualReceiver.getattr(self.selector)
        selectorMethod(**actualArguments)
