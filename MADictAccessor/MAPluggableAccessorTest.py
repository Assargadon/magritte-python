from unittest import TestCase, main
from MADictAccessor.MAPluggableAccessor_class import MAPluggableAccessor as map


class MAPluggableAccessorTest(TestCase):

    def test_canRead_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(2, 3)
        self.assertEqual(m.canRead(d), 2)

    def test_canRead_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(4, 5)
        self.assertEqual(m.canRead(d), 4)

    def test_canWrite_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(2, 3)
        self.assertEqual(m.canWrite(d), 3)

    def test_canWrite_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(4, 5)
        self.assertEqual(m.canWrite(d), 5)

    def test_read_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(2, 3)
        self.assertEqual(m.read(d), 11)

    def test_read_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(4, 5)
        self.assertEqual(m.read(d), None)

    def test_write_plus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(3, 3)
        m.write(d, 7)
        self.assertEqual(m.read(d), 7)

    def test_write_minus(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(5, 5)
        m.write(d, 7)
        self.assertEqual(m.read(d), 7)

    def test_getReadBlock(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(2, 3)
        self.assertEqual(m.readBlock, 2)

    def test_setReadBlock(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(4, 5)
        m.readBlock = 3
        self.assertEqual(m.readBlock, 3)

    def test_getWriteBlock(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(2, 3)
        self.assertEqual(m.writeBlock, 3)

    def test_setWriteBlock(self):
        d = {1: 10, 2: 11, 3: 13}
        m = map(4, 5)
        m.writeBlock = 6
        self.assertEqual(m.writeBlock, 6)

    def test_isAbstract(self):
        self.assertEqual(map.isAbstract(), False)
