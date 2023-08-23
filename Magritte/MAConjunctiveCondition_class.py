
from MACondition_class import MACondition


class MAConjunctiveCondition(MACondition):

    def __init__(self, conditions=None):
        self.conditions = [] if conditions is None else conditions

    def andCondition(self, aCondition):
        self.conditions.append(aCondition)
        return self

    def value(self, anObject):
        return all(condition.value(anObject) for condition in self.conditions)

