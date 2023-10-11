from unittest import TestCase
from . MAMethodReaderAccessor_class import MAMethodReaderAccessor

class MethodReadable:

    def __init__(self, aValue):
        self.value = aValue

    def AccessMethod(self):
        return self.value

class MAMethodReaderAccessorTest(TestCase):

    def setUp(self):
        self.Value = 10
        self.Model = MethodReadable(self.Value)
        self.MethodName = "AccessMethod"
        self.Accessor = MAMethodReaderAccessor(self.MethodName)

    def test_canRead(self):
        self.assertEqual(self.Accessor.canRead(self.Model), True)

        wrong_name_accessor = MAMethodReaderAccessor("blah-blah")
        self.assertEqual(wrong_name_accessor.canRead(self.Model), False)

    def test_canWrite(self):
        self.assertEqual(self.Accessor.canWrite(self.Model), False)

    def test_read(self):
        self.assertEqual(self.Accessor.read(self.Model), self.Value)

    def test_write(self):
        self.assertEqual(self.Accessor.write(self.Model, 0), None)

