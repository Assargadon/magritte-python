from unittest import TestCase
from Magritte.MANullAccessor_class import MANullAccessor


class MANullAccessorTest(TestCase):

    def test_isAbstract(self):
        self.assertEqual(MANullAccessor.isAbstract(), False)

    def test_read(self):
        aModel = {1: 10, 2: 11, 3: 12}
        inst = MANullAccessor()
        self.assertRaises(Exception, inst.read, aModel)

    def test_write(self):
        aModel = {1: 10, 2: 11, 3: 12}
        inst = MANullAccessor()
        self.assertRaises(Exception, inst.write, aModel, 3)

    def test_getUuid(self):
        inst = MANullAccessor()
        self.assertEqual(type(inst.uuid), list)

    def test_setUuid(self):
        inst = MANullAccessor()
        inst.uuid = 3
        self.assertEqual(inst.uuid, 3)

    def test_comparison_positive(self):
        inst1 = MANullAccessor()
        inst2 = MANullAccessor()

        inst1.uuid = inst2.uuid

        self.assertEqual(inst1 == inst2, True)

    def test_comparison_negative(self):
        inst1 = MANullAccessor()
        inst2 = MANullAccessor()

        self.assertEqual(inst1 == inst2, False)

    def test_canRead(self):
        aModel = {1: 11, 2: 12, 3: 13}
        inst = MANullAccessor()

        self.assertEqual(inst.canRead(aModel), False)

    def test_canWrite(self):
        aModel = {1: 11, 2: 12, 3: 13}
        inst = MANullAccessor()

        self.assertEqual(inst.canWrite(aModel), False)