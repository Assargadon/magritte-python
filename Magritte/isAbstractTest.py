from unittest import TestCase
from glob import glob
import re

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

class AbstractTest(TestCase):

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

    forcedAbstract = [
        MADescription,
        MAElementDescription,
        MAMagnitudeDescription,
        MANumberDescription,
        MAIntDescription,
        MAFloatDescription,
        MADurationDescription,
        MADateAndTimeDescription,
        MAReferenceDescription,
        MAStringDescription
    ]

    forcedNonAbstract = [
        MAOptionDescription,
        MARelationDescription
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

    def has_subclass(self, aClass):
        return len(aClass.__subclasses__()) > 0

    def test_abstract_descriptors(self):
        for desc in self.descriptors_to_test:
            if desc in self.forcedAbstract:
                self.assertEqual(self.has_subclass(desc), desc.isAbstract())

