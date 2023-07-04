from unittest import TestCase
from Magritte.MAIdentityAccessor_class import MAIdentityAccessor

class MAIdentityAccessorTest(TestCase):

    def test_canRead(self):
        aModel = {1: 10, 2: 11, 3: 12}
        inst = MAIdentityAccessor()
        self.assertEqual(inst.canRead(aModel), True)

    def test_canWrite(self):
        aModel = {1: 11, 2: 12, 3: 13}
        inst = MAIdentityAccessor()

        self.assertEqual(inst.canWrite(aModel), False)

    def test_read(self):
        aModel = {1: 10, 2: 11, 3: 12}
        inst = MAIdentityAccessor()
        self.assertEqual(inst.read(aModel), aModel)

    def test_write(self):
        aModel = {1: 10, 2: 11, 3: 12}
        inst = MAIdentityAccessor()
        self.assertRaises(Exception, inst.write, aModel, 3)

    def test_isAbstract(self):
        self.assertEqual(MAIdentityAccessor.isAbstract(), False)
