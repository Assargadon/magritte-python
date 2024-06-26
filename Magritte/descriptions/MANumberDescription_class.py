from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from Magritte.MACondition import MACondition


class MANumberDescription(MAMagnitudeDescription):

    def bePositive(self):
         self.addCondition(MACondition.model>0,
                            label="Positive number is required")

    def acceptMagritte(self, aVisitor):
        aVisitor.visitNumberDescription(self)
