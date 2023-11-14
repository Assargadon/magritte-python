from unittest import TestCase
from glob import glob
import re

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
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAUrlDescription_class import MAUrlDescription
from Magritte.descriptions.MAMemoDescription_class import MAMemoDescription

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
