from unittest import TestCase
from Magritte.MAIdentityAccessor_class import MAIdentityAccessor

class MAIdentityAccessorTest(TestCase):

    def test_canRead(self):
        d = {1: 10, 2: 11, 3: 12}
        m = MAIdentityAccessor()
        self.assertEqual(m.canRead(d), True)

    def test_read(self):
        d = {1: 10, 2: 11, 3: 12}
        m = MAIdentityAccessor()
        self.assertEqual(m.read(d), d)

    def test_write(self):
        d = {1: 10, 2: 11, 3: 12}
        m = MAIdentityAccessor()
        self.assertRaises(Exception, m.write(d, 3))

    def test_isAbstract(self):
        self.assertEqual(MAIdentityAccessor.isAbstract(), False)
