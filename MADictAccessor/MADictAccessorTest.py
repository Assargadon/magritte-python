from unittest import TestCase, main
from MADictAccessor.MADictAccessor_class import MADictAccessor as mad


class MADictAccessorTest(TestCase):

    def test_canRead(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        self.assertEqual(m.canRead(d), True)

    def test_canWrite(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        self.assertEqual(m.canWrite(d), True)

    def test_read(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        self.assertEqual(m.read(d), 11)

    def test_write(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        m.write(d, 7)
        self.assertEqual(m.read(d), 7)

    def test_getKey(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        t = m.getKey
        self.assertEqual(t, 2)

    def test_setKey(self):
        d = {1: 10, 2: 11, 3: 13}
        m = mad(2)
        m.setKey = 3
        self.assertEqual(m.getKey, 3)

    def test_isAbstract(self):
        self.assertEqual(mad.isAbstract(), False)


if __name__ == '__main__':
    main()