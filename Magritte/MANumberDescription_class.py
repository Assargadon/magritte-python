from MAMagnitudeDescription_class import MAMagnitudeDescription


class MANumberDescription(MAMagnitudeDescription):

    @classmethod
    def isAbstract(cls):
        return True

    #addCondition is not implemented yet

    # def be_integer(self):
    #     self.addCondition(condition="is_integer",
    #                        label="No integer was entered")
    #
    # def be_negative(self):
    #     self.addCondition(condition="negative",
    #                        label="No negative number was entered")
    #
    # def be_positive(self):
    #     self.addCondition(condition="positive",
    #                        label="No positive number was entered")
