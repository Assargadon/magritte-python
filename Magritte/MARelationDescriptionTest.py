from unittest import TestCase
from MARelationDescription_class import MARelationDescription
from MAPriorityContainer_class import MAPriorityContainer
from MAAccessor_class import MAAccessor
from MADictAccessor_class import MADictAccessor
from MANullAccessor_class import MANullAccessor
from MAStringDescription_class import MAStringDescription


class MARelationDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MARelationDescription()

    def test_copy(self):
        self.assertEqual(self.inst1.__copy__(), self.inst1)

    def test_classes(self):
        self.assertEqual(self.inst1.classes, set())
        self.inst1.classes = [int, bool, str]
        self.assertEqual(self.inst1.classes, [int, bool, str])

    def test_commonClass(self):
        self.assertIsInstance(self.inst1.commonClass(), MAPriorityContainer)
        self.inst1.classes = [MADictAccessor, MAAccessor, MANullAccessor]
        self.assertEqual(self.inst1.commonClass(), MAAccessor)

    def test_reference(self):
        self.assertIsInstance(self.inst1.reference(), MAStringDescription)
