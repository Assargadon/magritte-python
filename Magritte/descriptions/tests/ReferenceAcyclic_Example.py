
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor
from Magritte.visitors.MAVisitor_class import MAVisitor


class AcyclicTestVisitor(MAVisitor):
    def __init__(self, printPadding=0):
        super().__init__()
        self.printPadding = printPadding
        self.prefix = ' ' * printPadding

    def printDescriptionOpening(self, anObject, suffix=''):
        print(f'{self.prefix}<{anObject.__class__.__name__} name="{anObject.name}"{suffix}>')

    def printDescriptionFinal(self, anObject):
        print(f'{self.prefix}</{anObject.__class__.__name__}>')

    def visitDescription(self, anObject):
        self.printDescriptionOpening(anObject, suffix='/')

    def visitContainer(self, anObject):
        self.printDescriptionOpening(anObject)
        print(f'{self.prefix}  <children of="{anObject.name}">')
        childAcyclicTestVisitor = AcyclicTestVisitor(self.printPadding + 4)
        for child in anObject.children:
            child.acceptMagritte(childAcyclicTestVisitor)
        print(f'{self.prefix}  </children>')
        self.printDescriptionFinal(anObject)

    def visitReferenceDescription(self, anObject):
        self.printDescriptionOpening(anObject)
        print(f'{self.prefix}  <acyclicDescription of="{anObject.name}">')
        childAcyclicTestVisitor = AcyclicTestVisitor(self.printPadding + 4)
        anObject.reference.acyclicDescription.acceptMagritte(childAcyclicTestVisitor)
        print(f'{self.prefix}  </acyclicDescription>')
        self.printDescriptionFinal(anObject)


def main():
    provider = TestEnvironmentProvider()
    hostDescriptor = TestModelDescriptor.description_for("Host")
    #print(hostDescriptor)
    #print(hostDescriptor.acyclicDescription)
    acyclicTestVisitor = AcyclicTestVisitor()
    hostDescriptor.acceptMagritte(acyclicTestVisitor)


if __name__ == "__main__":
    main()


