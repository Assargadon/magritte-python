from unittest import TestCase
from glob import glob
import re
from MAVisitor_class import MAVisitor

from MADescription_class import MADescription
from MAElementDescription_class import MAElementDescription
from MAMagnitudeDescription_class import MAMagnitudeDescription
from MANumberDescription_class import MANumberDescription
from MAIntDescription_class import MAIntDescription
from MAFloatDescription_class import MAFloatDescription
from MADurationDescription_class import MADurationDescription
from MADateAndTimeDescription_class import MADateAndTimeDescription
from MAOptionDescription_class import MAOptionDescription
from MAReferenceDescription_class import MAReferenceDescription
from MARelationDescription_class import MARelationDescription
from MAStringDescription_class import MAStringDescription


class MATestingVisitor(MAVisitor):
    def __init__(self):
        self.visited_methods = []

    def visitDescription(self, anObject):
        self.visited_methods.append(MADescription.__name__)
        super().visitDescription(anObject)

    def visitElementDescription(self, anObject):
        self.visited_methods.append(MAElementDescription.__name__)
        super().visitElementDescription(anObject)

    def visitMagnitudeDescription(self, anObject):
        self.visited_methods.append(MAMagnitudeDescription.__name__)
        super().visitMagnitudeDescription(anObject)

    def visitOptionDescription(self, anObject):
        self.visited_methods.append(MAOptionDescription.__name__)
        super().visitOptionDescription(anObject)

    def visitReferenceDescription(self, anObject):
        self.visited_methods.append(MAReferenceDescription.__name__)
        super().visitReferenceDescription(anObject)

    def visitRelationDescription(self, anObject):
        self.visited_methods.append(MARelationDescription.__name__)
        super().visitRelationDescription(anObject)

    def visitStringDescription(self, anObject):
        self.visited_methods.append(MAStringDescription.__name__)
        super().visitStringDescription(anObject)


class MATestingVisitAllVisitor(MAVisitor):
        def __init__(self):
            self.visited_descriptors = []

        def visit(self, descriptor):
            self.visited_descriptors.append(descriptor)


class MAVisitorTest(TestCase):

    descriptors_to_test = [
        MADescription,
        MAElementDescription,
        MAMagnitudeDescription,
        MANumberDescription,
        MAIntDescription,
        MAFloatDescription,
        MADurationDescription,
        MADateAndTimeDescription,
        MAOptionDescription,
        MAReferenceDescription,
        MARelationDescription,
        MAStringDescription
    ]  # Add other classes here

    descriptors_to_ignore = [

    ]

    def setUp(self):
        # Проверка, что не появились новые классы дескрипторов. При появлении - выдаст assertion.
        descriptions_file_list = glob('MA*Description_class.py')
        descriptors_all = [x.__name__ for x in (self.descriptors_to_test + self.descriptors_to_ignore)]
        pattern = "|".join(map(re.escape, descriptors_all))
        regex = re.compile(pattern)

        for file_name in descriptions_file_list:
            match = regex.search(file_name)
            if match is None:
                self.assertTrue(False, f'{file_name} found. Add the class to one of then descriptors_to_test or descriptors_to_ignore lists')

    def get_inheritance_chain(self, cls):
        return [base.__name__ for base in cls.__mro__ if base != object]

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
    
    
