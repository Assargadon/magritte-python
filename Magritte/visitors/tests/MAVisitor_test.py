from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.descriptions.tests.AbstractTestForAllDescriptions import AbstractTestForAllDescriptions
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from Magritte.descriptions.MANumberDescription_class import MANumberDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MAOptionDescription_class import MAOptionDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAUrlDescription_class import MAUrlDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAMemoDescription_class import MAMemoDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAPriorityContainer_class import MAPriorityContainer

class MATestingVisitor(MAVisitor):
    def __init__(self):
        self.visited_methods = []

    def visitDescription(self, anObject):
        self.visited_methods.append(MADescription.__name__)
        super().visitDescription(anObject)

    def visitElementDescription(self, anObject):
        self.visited_methods.append(MAElementDescription.__name__)
        super().visitElementDescription(anObject)

    def visitBooleanDescription(self, anObject):
        self.visited_methods.append(MABooleanDescription.__name__)
        super().visitBooleanDescription(anObject)

    def visitMagnitudeDescription(self, anObject):
        self.visited_methods.append(MAMagnitudeDescription.__name__)
        super().visitMagnitudeDescription(anObject)

    def visitNumberDescription(self, anObject):
        self.visited_methods.append(MANumberDescription.__name__)
        super().visitNumberDescription(anObject)

    def visitIntDescription(self, anObject):
        self.visited_methods.append(MAIntDescription.__name__)
        super().visitIntDescription(anObject)

    def visitFloatDescription(self, anObject):
        self.visited_methods.append(MAFloatDescription.__name__)
        super().visitFloatDescription(anObject)

    def visitDateAndTimeDescription(self, anObject):
        self.visited_methods.append(MADateAndTimeDescription.__name__)
        super().visitDateAndTimeDescription(anObject)

    def visitDateDescription(self, anObject):
        self.visited_methods.append(MADateDescription.__name__)
        super().visitDateDescription(anObject)

    def visitDurationDescription(self, anObject):
        self.visited_methods.append(MADurationDescription.__name__)
        super().visitDurationDescription(anObject)

    def visitReferenceDescription(self, anObject):
        self.visited_methods.append(MAReferenceDescription.__name__)
        super().visitReferenceDescription(anObject)

    def visitOptionDescription(self, anObject):
        self.visited_methods.append(MAOptionDescription.__name__)
        super().visitOptionDescription(anObject)

    def visitSingleOptionDescription(self, anObject):
        self.visited_methods.append(MASingleOptionDescription.__name__)
        super().visitSingleOptionDescription(anObject)

    def visitRelationDescription(self, anObject):
        self.visited_methods.append(MARelationDescription.__name__)
        super().visitRelationDescription(anObject)

    def visitTimeDescription(self, anObject):
        self.visited_methods.append(MATimeDescription.__name__)
        super().visitTimeDescription(anObject)

    def visitToOneRelationDescription(self, anObject):
        self.visited_methods.append(MAToOneRelationDescription.__name__)
        super().visitToOneRelationDescription(anObject)

    def visitToManyRelationDescription(self, anObject):
        self.visited_methods.append(MAToManyRelationDescription.__name__)
        super().visitToManyRelationDescription(anObject)

    def visitUrlDescription(self, anObject):
        self.visited_methods.append(MAUrlDescription.__name__)
        super().visitUrlDescription(anObject)

    def visitStringDescription(self, anObject):
        self.visited_methods.append(MAStringDescription.__name__)
        super().visitStringDescription(anObject)

    def visitMemoDescription(self, anObject):
        self.visited_methods.append(MAMemoDescription.__name__)
        super().visitMemoDescription(anObject)

    def visitContainer(self, aMAContainer):
        self.visited_methods.append(MAContainer.__name__)
        super().visitContainer(aMAContainer)

    def visitPriorityContainer(self, aMAPriorityContainer):
        self.visited_methods.append(MAPriorityContainer.__name__)
        super().visitPriorityContainer(aMAPriorityContainer)


class MATestingVisitAllVisitor(MAVisitor):
        def __init__(self):
            self.visited_descriptors = []

        def visit(self, descriptor):
            self.visited_descriptors.append(descriptor)


class MAVisitorTest(AbstractTestForAllDescriptions):

    def get_inheritance_chain(self, cls):
        return [base.__name__ for base in cls.__mro__ if issubclass(base, MADescription)]

    def check_descriptor(self, descriptor):
        # Get expected inheritance chain
        expected_chain = self.get_inheritance_chain(descriptor)

        # Create a visitor and visit the description
        visitor = MATestingVisitor()
        description_instance = descriptor()
        visitor.visit(description_instance)

        # Assert
        self.assertEqual(visitor.visited_methods, expected_chain, f"For {descriptor.__name__}, visitor did not correctly mimic inheritance chain")
        # print(visitor.visited_methods)

    def test_visitor_mimics_inheritance(self):

        for descriptor in self.descriptors_to_test:
            with self.subTest(descriptor=descriptor):
                self.check_descriptor(descriptor)

    def test_visitAll(self):
    
        testing_visitor = MATestingVisitAllVisitor()
        testing_visitor.visitAll(self.descriptors_to_test)

        self.assertEqual(set(testing_visitor.visited_descriptors), set(self.descriptors_to_test),
            "The visitor's visit method did not visit all the expected descriptors")
    
    
