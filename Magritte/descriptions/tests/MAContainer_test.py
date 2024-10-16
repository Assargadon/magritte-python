from unittest import TestCase
from copy import copy

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.descriptions.MAStringDescription_class import MAStringDescription


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
        desc = MAContainer()
        desc += MAStringDescription(name="first", label="First Field")
        desc += MAStringDescription(label="nameless #2")
        desc += MAStringDescription(name="second", label="Second Field")
        desc += MAStringDescription(label="nameless #1")

        self.assertEqual(desc["first"].label, "First Field")
        self.assertEqual(desc["second"].label, "Second Field")
        with self.assertRaises(TypeError):
            _ = desc[0]
        with self.assertRaises(KeyError):
            _ = desc["third"]

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
        self.assertEqual(self.inst1.children[2] if 2 < len(self.inst1) else 'index > len', 3)
        self.assertEqual(self.inst1.children[7] if 7 < len(self.inst1) else 'index > len', 'index > len')

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

    def test_iter(self):
        self.inst1.setChildren([1, 2, 3, 4])
        self.assertEqual([item for item in self.inst1], [1, 2, 3, 4])

class MAContainerInheritanceTest(TestCase):

    def setUp(self):
        self.ancestor = MAContainer(name='Ancestor')
        self.ancestor += MAStringDescription(name='string1', label='String 1')
        self.ancestor += MAStringDescription(label='String 2')
        self.ancestor += MAStringDescription(name='string3', label='String 3')
        self.ancestor += MAStringDescription(label='String 4')
        self.ancestor += MAStringDescription(name='string5', label='String 5')

    def test_inheritFrom_copy(self):
        descendant = MAContainer(name='Descendant')
        descendant.inheritFrom(self.ancestor)
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children))
        for i in range(len(self.ancestor.children)):
            self.assertEqual(self.ancestor.children[i].name, descendant.children[i].name)
            self.assertEqual(self.ancestor.children[i].label, descendant.children[i].label)

    def test_inheritFrom_update(self):
        descendant = MAContainer(name='Descendant')
        descendant.inheritFrom(self.ancestor, override=[MAStringDescription(name='string1', label='Updated String 1')])
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children))
        for i in range(len(self.ancestor.children)):
            if self.ancestor.children[i].name == 'string1':
                self.assertEqual(descendant.children[i].label, 'Updated String 1')
            else:
                self.assertEqual(self.ancestor.children[i].name, descendant.children[i].name)
                self.assertEqual(self.ancestor.children[i].label, descendant.children[i].label)

    def test_inheritFrom_remove(self):
        descendant = MAContainer(name='Descendant')
        removed_elements = ['string1']
        descendant.inheritFrom(self.ancestor, remove=removed_elements)
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children) - len(removed_elements))
        # parallel iteration over two lists skipping removed item
        a_child_iter = iter(self.ancestor.children)
        d_child_iter = iter(descendant.children)
        for a_child in a_child_iter:
            if a_child.name in removed_elements:
                continue
            d_child = next(d_child_iter)
            self.assertEqual(a_child.name, d_child.name)
            self.assertEqual(a_child.label, d_child.label)

    def test_inheritFrom_insert(self):
        descendant = MAContainer(name='Descendant')
        descendant.inheritFrom(self.ancestor, override=[MAStringDescription(name='string6', label='String 6')])
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children) + 1)
        # parallel iteration over two lists skipping removed item
        a_child_iter = iter(self.ancestor.children)
        d_child_iter = iter(descendant.children)
        for a_child in a_child_iter:
            d_child = next(d_child_iter)
            self.assertEqual(a_child.name, d_child.name)
            self.assertEqual(a_child.label, d_child.label)
        d_child = next(d_child_iter)
        self.assertEqual(d_child.name, 'string6')
        self.assertEqual(d_child.label, 'String 6')

    def test_inheritFrom_update_remove(self):
        descendant = MAContainer(name='Descendant')
        removed_elements = ['string1', 'string3']
        descendant.inheritFrom(
            self.ancestor,
            override=[MAStringDescription(name='string5', label='Updated String 5')],
            remove=removed_elements
            )
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children) - len(removed_elements))
        # parallel iteration over two lists skipping removed item
        a_child_iter = iter(self.ancestor.children)
        d_child_iter = iter(descendant.children)
        for a_child in a_child_iter:
            if a_child.name in removed_elements:
                continue
            d_child = next(d_child_iter)
            self.assertEqual(a_child.name, d_child.name)
            if a_child.name == 'string5':
                self.assertEqual(d_child.label, 'Updated String 5')
            else:
                self.assertEqual(a_child.label, d_child.label)

    def test_inheritFrom_update_remove_insert(self):
        descendant = MAContainer(name='Descendant')
        removed_elements = ['string1', 'string3']
        descendant.inheritFrom(
            self.ancestor,
            override=[
                MAStringDescription(name='string5', label='Updated String 5'),
                MAStringDescription(name='string6', label='String 6')
                ],
            remove=removed_elements
            )
        self.assertEqual(descendant.ancestor, self.ancestor)
        self.assertEqual(len(descendant.children), len(self.ancestor.children) - len(removed_elements) + 1)
        # parallel iteration over two lists skipping removed item
        a_child_iter = iter(self.ancestor.children)
        d_child_iter = iter(descendant.children)
        for a_child in a_child_iter:
            if a_child.name in removed_elements:
                continue
            d_child = next(d_child_iter)
            self.assertEqual(a_child.name, d_child.name)
            if a_child.name == 'string5':
                self.assertEqual(d_child.label, 'Updated String 5')
            else:
                self.assertEqual(a_child.label, d_child.label)
        d_child = next(d_child_iter)
        self.assertEqual(d_child.name, 'string6')
        self.assertEqual(d_child.label, 'String 6')
