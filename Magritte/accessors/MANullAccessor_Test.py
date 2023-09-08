from unittest import TestCase
from Magritte.accessors.MANullAccessor_class import MANullAccessor


class MANullAccessorTest(TestCase):

    def test_read(self):
        aModel = {1: 10, 2: 11, 3: 12}
        nullAccessor = MANullAccessor()
        self.assertRaises(Exception, nullAccessor.read, aModel)

    def test_write(self):
        aModel = {1: 10, 2: 11, 3: 12}
        nullAccessor = MANullAccessor()
        self.assertRaises(Exception, nullAccessor.write, aModel, 3)

    def test_getUuid(self):
        nullAccessor = MANullAccessor()
        self.assertEqual(type(nullAccessor.uuid), list)

    def test_setUuid(self):
        nullAccessor = MANullAccessor()
        nullAccessor.uuid = 3
        self.assertEqual(nullAccessor.uuid, 3)

    def test_comparison_positive(self):
        nullAccessor1 = MANullAccessor()
        nullAccessor2 = MANullAccessor()

        nullAccessor1.uuid = nullAccessor2.uuid

        self.assertEqual(nullAccessor1 == nullAccessor2, True)

    def test_comparison_negative(self):
        nullAccessor1 = MANullAccessor()
        nullAccessor2 = MANullAccessor()

        self.assertEqual(nullAccessor1 == nullAccessor2, False)

    def test_canRead(self):
        aModel = {1: 11, 2: 12, 3: 13}
        nullAccessor = MANullAccessor()

        self.assertEqual(nullAccessor.canRead(aModel), False)

    def test_canWrite(self):
        aModel = {1: 11, 2: 12, 3: 13}
        nullAccessor = MANullAccessor()

        self.assertEqual(nullAccessor.canWrite(aModel), False)
