from unittest import TestCase
from MAIdentityAccessor_class import MAIdentityAccessor

class MAIdentityAccessorTest(TestCase):

    def test_canRead(self):
        aModel = {1: 10, 2: 11, 3: 12}
        identityAccessor = MAIdentityAccessor()
        self.assertEqual(identityAccessor.canRead(aModel), True)

    def test_canWrite(self):
        aModel = {1: 11, 2: 12, 3: 13}
        identityAccessor = MAIdentityAccessor()

        self.assertEqual(identityAccessor.canWrite(aModel), False)

    def test_read(self):
        aModel = {1: 10, 2: 11, 3: 12}
        identityAccessor = MAIdentityAccessor()
        self.assertEqual(identityAccessor.read(aModel), aModel)

    def test_write(self):
        aModel = {1: 10, 2: 11, 3: 12}
        identityAccessor = MAIdentityAccessor()
        self.assertRaises(Exception, identityAccessor.write, aModel, 3)
