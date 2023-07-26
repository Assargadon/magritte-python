from unittest import TestCase
from Magritte.MAPriorityContainerDescription_class import MAPriorityContainerDescription


class MAPriorityContainerDescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MAPriorityContainerDescription()
        self.inst1.setChildren([1, 2, 3])

    def test_append(self):
        self.inst1.append(4)
        self.assertEqual(self.inst1.children, [1, 2, 3, 4])

    def test_extend(self):
        self.inst1.extend([4, 5, 6])
        self.assertEqual(self.inst1.children, [1, 2, 3, 4, 5, 6])

    def test_moveDown(self):
        self.assertRaises(NotImplementedError, self.inst1.moveDown, 4)

    def test_moveUp(self):
        self.assertRaises(NotImplementedError, self.inst1.moveUp, 4)

    def test_resort(self):
        self.inst1.resort()
        self.assertEqual(self.inst1.children, [1, 2, 3])
