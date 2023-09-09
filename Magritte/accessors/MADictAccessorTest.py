from unittest import TestCase
from . MADictAccessor_class import MADictAccessor


class MADictAccessorTest(TestCase):

    def test_canRead_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        self.assertEqual(m.canRead(d), True)

    def test_canRead_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(4)
        self.assertEqual(m.canRead(d), True)

    def test_canWrite_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        self.assertEqual(m.canWrite(d), True)

    def test_canWrite_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(4)
        self.assertEqual(m.canWrite(d), True)

    def test_read_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        self.assertEqual(m.read(d), 11)

    def test_read_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(4)
        self.assertEqual(m.read(d), None)

    def test_write_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        m.write(d, 7)
        self.assertEqual(m.read(d), 7)

    def test_write_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(4)
        m.write(d, 7)
        self.assertEqual(m.read(d), 7)

    def test_getKey(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        self.assertEqual(m.key, 2)

    def test_setKey(self):
        d = {1: 10, 2: 11, 3: 13}
        m = MADictAccessor(2)
        m.key = 3
        self.assertEqual(m.key, 3)

    def test_name(self):
        m = MADictAccessor(2)
        self.assertEqual(m.name, 2)
