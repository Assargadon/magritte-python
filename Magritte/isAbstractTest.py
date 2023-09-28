from unittest import TestCase
from glob import glob
import re

from MADescription_class import MADescription
from MAElementDescription_class import MAElementDescription
from MABooleanDescription_class import MABooleanDescription
from MAMagnitudeDescription_class import MAMagnitudeDescription
from MANumberDescription_class import MANumberDescription
from MAIntDescription_class import MAIntDescription
from MAFloatDescription_class import MAFloatDescription
from MADurationDescription_class import MADurationDescription
from MADateAndTimeDescription_class import MADateAndTimeDescription
from MADateDescription_class import MADateDescription
from MAOptionDescription_class import MAOptionDescription
from MAPasswordDescription_class import MAPasswordDescription
from MAReferenceDescription_class import MAReferenceDescription
from MARelationDescription_class import MARelationDescription
from MASingleOptionDescription_class import MASingleOptionDescription
from MAStringDescription_class import MAStringDescription
from MATimeDescription_class import MATimeDescription
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAToOneRelationDescription_class import MAToOneRelationDescription
from MAUrlDescription_class import MAUrlDescription

class AbstractTest(TestCase):

    descriptors_to_test = [
        MADescription,
        MAElementDescription,
        MABooleanDescription,
        MAMagnitudeDescription,
        MANumberDescription,
        MAIntDescription,
        MAFloatDescription,
        MADurationDescription,
        MADateDescription,
        MADateAndTimeDescription,
        MAOptionDescription,
        MAPasswordDescription,
        MAReferenceDescription,
        MARelationDescription,
        MASingleOptionDescription,
        MAStringDescription,
        MATimeDescription,
        MAToManyRelationDescription,
        MAToOneRelationDescription,
        MAUrlDescription
    ]  # Add other classes here

    descriptors_to_ignore = [

    ]

    # абстрактные классы у которых не реализованы потомки, они проверяются насильно
    forcedAbstract = [
        MAUrlDescription
    ]

    # неабстрактные классы, они проверяются насильно
    forcedNonAbstract = [
        MAStringDescription
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
            with self.subTest(desc):
                if desc in self.forcedAbstract:
                    self.assertTrue(desc.isAbstract())
                elif desc in self.forcedNonAbstract:
                    self.assertFalse(desc.isAbstract())
                else:
                    self.assertEqual(self.has_subclass(desc), desc.isAbstract())
    

