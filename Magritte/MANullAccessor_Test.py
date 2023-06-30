from unittest import TestCase
from Magritte.MANullAccessor_class import MANullAccessor


class MANullAccessorTest(TestCase):

    def test_read(self):
        d = {1: 10, 2: 11, 3: 12}
        m = MANullAccessor()
        self.assertRaises(Exception, m.read(d))

    def test_write(self):
        d = {1: 10, 2: 11, 3: 12}
        m = MANullAccessor()
        self.assertRaises(Exception, m.write(d, 3))

    def test_getUuid(self):
        m = MANullAccessor()
        self.assertEqual(type(m.uuid), list)

    def test_setUuid(self):
        m = MANullAccessor()
        m.uuid = 3
        self.assertEqual(m.uuid, 3)