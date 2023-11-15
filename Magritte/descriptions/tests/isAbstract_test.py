from Magritte.descriptions.tests.AbstractTestForAllDescriptions import AbstractTestForAllDescriptions

from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAUrlDescription_class import MAUrlDescription

class AbstractTest(AbstractTestForAllDescriptions):

    # абстрактные классы у которых не реализованы потомки, они проверяются насильно
    forcedAbstract = [
        MAUrlDescription
    ]

    # неабстрактные классы, они проверяются насильно
    forcedNonAbstract = [
        MAStringDescription
    ]

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
    

