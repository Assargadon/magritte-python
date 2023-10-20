from unittest import TestCase
from glob import glob
import re

from descriptions.MADescription_class import MADescription
from descriptions.MAElementDescription_class import MAElementDescription
from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription
from descriptions.MANumberDescription_class import MANumberDescription
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MAFloatDescription_class import MAFloatDescription
from descriptions.MADurationDescription_class import MADurationDescription
from descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from descriptions.MADateDescription_class import MADateDescription
from descriptions.MAOptionDescription_class import MAOptionDescription
from descriptions.MAReferenceDescription_class import MAReferenceDescription
from descriptions.MARelationDescription_class import MARelationDescription
from descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MATimeDescription_class import MATimeDescription
from descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from descriptions.MAUrlDescription_class import MAUrlDescription
from descriptions.MAMemoDescription_class import MAMemoDescription

class AbstractTestForAllDescriptions(TestCase):

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
        MAReferenceDescription,
        MARelationDescription,
        MASingleOptionDescription,
        MAStringDescription,
        MATimeDescription,
        MAToManyRelationDescription,
        MAToOneRelationDescription,
        MAUrlDescription,
        MAMemoDescription
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
                self.assertTrue(False,
                                f'{file_name} found. Add the class to one of then descriptors_to_test or descriptors_to_ignore lists')
