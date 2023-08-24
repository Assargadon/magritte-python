from unittest import TestCase
from MAPriorityContainer_class import MAPriorityContainer


class MAPriorityContainerTest(TestCase):

    def setUp(self):
        self.inst1 = MAPriorityContainer()
        self.inst1.setChildren([1, 3, 2])

    def test_append(self):
        self.inst1.append(4)
        self.assertEqual(self.inst1.children, [1, 2, 3, 4])

    def test_extend(self):
        self.inst1.extend([6, 4, 5])
        self.assertEqual(self.inst1.children, [1, 2, 3, 4, 5, 6])

    def test_resort(self):
        self.inst1.resort()
        self.assertEqual(self.inst1.children, [1, 2, 3])
