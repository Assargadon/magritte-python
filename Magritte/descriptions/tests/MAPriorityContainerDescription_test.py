from unittest import TestCase

from Magritte.descriptions.MAPriorityContainer_class import MAPriorityContainer
import Magritte.descriptions.tests.MADescription_test as MADescription_test


class TestProperties_of_MAPriorityContainerDescription(MADescription_test.TestProperties_of_MADescription):
    def get_description_instance_to_test(self):
        return MAPriorityContainer()



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
