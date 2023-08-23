
from MACondition_class import MACondition


class MANegationCondition(MACondition):

    def __init__(self, aCondition):
        self.condition = aCondition

    def value(self, anObject):
        return not self.condition.value(anObject)

