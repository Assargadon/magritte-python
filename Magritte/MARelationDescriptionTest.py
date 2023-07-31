from unittest import TestCase
from Magritte.MARelationDescription_class import MARelationDescription
from Magritte.MAPriorityContainer_class import MAPriorityContainer
from Magritte.MAAccessor_class import MAAccessor
from Magritte.MADictAccessor_class import MADictAccessor
from Magritte.MANullAccessor_class import MANullAccessor
from Magritte.MAStringDescription_class import MAStringDescription


class MARelationDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MARelationDescription()

    def test_copy(self):
        self.assertEqual(self.inst1.__copy__(), self.inst1)

    def test_defaultClasses(self):
        self.assertEqual(MARelationDescription.defaultClasses(), set())

    def test_getClasses(self):
        self.assertEqual(self.inst1.classes, set())

    def test_setClasses(self):
        self.inst1.classes = [int, bool, str]
        self.assertEqual(self.inst1.classes, [int, bool, str])

    def test_allClasses(self):
        self.inst1.classes = [int, bool, str]
        self.assertEqual(self.inst1.allClasses, [bool, int, str])

    def test_commonClass(self):
        self.assertEqual(isinstance(self.inst1.commonClass(), MAPriorityContainer), True)
        self.inst1.classes = [MAAccessor, MADictAccessor, MANullAccessor]
        self.assertEqual(self.inst1.commonClass(), MAAccessor)

    def test_reference(self):
        self.assertEqual(isinstance(self.inst1.reference, MAStringDescription), True)
