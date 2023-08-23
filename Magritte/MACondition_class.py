
from MAPluggableCondition_class import MAPluggableCondition
from MAConjunctiveCondition_class import MAConjunctiveCondition
from MANegationCondition_class import MANegationCondition


class MACondition:

    @classmethod
    def isAbstract(cls):
        return cls == MACondition

    @classmethod
    def receiverSelector(cls, anObject, aSelector):
        cls.receiverSelectorArgumentsIndex(anObject, aSelector, [None], 1)

    @classmethod
    def receiverSelectorArgumentsIndex(cls, anObject, aSelector, anArray, anInteger):
        if anInteger not in range(0, len(anArray)):
            self.error('Index out of bounds.')
        c = MAPluggableCondition()
        c.initializeReceiver(anObject)
        c.selector = aSelector
        c.arguments = anArray
        c.index = anInteger
        return c

    @classmethod
    def selector(cls, aSelector):
        cls.receiverSelectorArgumentsIndex(None, aSelector, [], 0)

    @classmethod
    def selectorArgument(cls, aSelector, anObject):
        cls.receiverSelectorArgumentsIndex(None, aSelector, [anObject], 0)

    def andCondition(self, aCondition):
        return MAConjunctiveCondition([self, aCondition])

    def orCondition(self, aCondition):
        return (self.notCondition().andCondition(aCondition.notCondition())).notCondition()

    def notCondition(self):
        return MANegationCondition(self)

    def numArgs(self):
        return 1

    def value(self, anObject):
        pass

