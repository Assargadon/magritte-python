from unittest import TestCase
from copy import copy

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor


class MAContainerTest(TestCase):

    def setUp(self):
        self.inst1 = MAContainer()
        self.inst2 = MAContainer()
        self.block1 = lambda x: x < 10
        self.block2 = lambda x, y: x < 10 and y < 10

    def test_eq(self):
        self.assertEqual(self.inst1 == self.inst2, False)
        self.assertEqual(self.inst1 == self.inst1, True)

    def test_iadd(self):
        self.inst1.__iadd__('exm')
        self.assertEqual(self.inst1.__contains__('exm'), True)

    def test_len(self):
        self.inst1 += 'exm1'
        self.inst1 += 'exm2'
        self.inst1 += 'exm3'
        self.inst1 += 'exm4'
        self.assertEqual(len(self.inst1), 4)

    def test_getitem(self):
        self.inst1 += 'exm1'
        self.inst1 += 'exm2'
        self.inst1 += 'exm3'
        self.inst1 += 'exm4'
        self.assertEqual(self.inst1[0], 'exm1')

    def test_copy(self):
        exm = copy(self.inst1)
        self.assertEqual(self.inst1 == exm, True)

    def test_defaultAccessor(self):
        self.assertEqual(isinstance(MAContainer.defaultAccessor(), MAIdentityAccessor), True)

    def test_getChildren(self):
        self.assertEqual(self.inst1.children, [])

    def test_setChildren(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.children, [1, 2, 3, 4])

    def test_isContainer(self):
        self.assertEqual(self.inst1.isContainer(), True)

    def test_notEmpty(self):
        self.assertEqual(self.inst1.notEmpty(), False)
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.notEmpty(), True)

    def test_isEmpty(self):
        self.assertEqual(self.inst1.isEmpty(), True)
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.isEmpty(), False)

    def test_hasChildren(self):
        self.assertEqual(self.inst1.hasChildren(), False)
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.hasChildren(), True)

    def test_append(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.inst1.append(5)
        self.assertEqual(self.inst1.children, [1, 2, 3, 4, 5])

    def test_extend(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.inst1.extend([5, 6, 7])
        self.assertEqual(self.inst1.children, [1, 2, 3, 4, 5, 6, 7])

    def test_withDescription(self):
        self.assertEqual(self.inst1.withDescription(123).children, [123])

    def test_withAllDescription(self):
        self.assertEqual(self.inst1.withAllDescriptions([1, 2, 3]).children, [1, 2, 3])

    def test_defaultCollection(self):
        self.assertEqual(MAContainer.defaultCollection(), [])

    def test_asContainer(self):
        self.assertEqual(self.inst1.asContainer(), self.inst1)

    def test_get(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1[2] if 2 < len(self.inst1) else 'index > len', 3)
        self.assertEqual(self.inst1[7] if 7 < len(self.inst1) else 'index > len', 'index > len')

    def test_allSatisfy(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.allSatisfy(self.block1), True)
        # self.inst2.setChildren([1, 2, [], 4])
        # self.assertEqual(self.inst2.allSatisfy(self.block), False)

    def test_anySatisfy(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.anySatisfy(self.block1), True)

    def test_collect(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.collect(self.block1).children, [True, True, True, True])

    def test_select(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.select(self.block1).children, [1, 2, 3, 4])
        self.inst2.setChildren([1, 2, 3, 40])
        self.assertEqual(self.inst2.select(self.block1).children, [1, 2, 3])

    def test_reject(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.reject(self.block1).children, [])
        self.inst2.setChildren([1, 2, 3, 40])
        self.assertEqual(self.inst2.reject(self.block1).children, [40])

    def test_copyEmpty(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.copyEmpty().children, [])

    def test_copyRange(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.copyRange(2, 3).children, [3, 4])

    def test_copyWithout(self):
        self.inst1.setChildren([1, 2, 3, 2])
        self.assertEqual(self.inst1.copyWithout(2).children, [1, 3])

    def test_copyWithoutAll(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.copyWithoutAll([2, 3, 4]).children, [1])

    def test_detect(self):
        self.inst1.setChildren([11, 2, 3, 4])
        self.assertEqual(self.inst1.detect(self.block1), 2)

    def test_detectIfNone(self):
        self.inst1.setChildren([11, 2, 3, 4])
        exceptionBlock = lambda: 'error'
        self.assertEqual(self.inst1.detectIfNone(self.block1, exceptionBlock), 2)
        self.inst2.setChildren([11, 22, 33, 44])
        self.assertEqual(self.inst2.detectIfNone(self.block1, exceptionBlock), 'error')

    def test_do(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.do(self.block1), None)

    def test_keysAndValuesDo(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual(self.inst1.keysAndValuesDo(self.block2), None)
