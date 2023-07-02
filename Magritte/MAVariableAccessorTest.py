from unittest import TestCase
from Magritte.MAVariableAccessor_class import MAVariableAccessor


class MAVariableAccessorTest(TestCase):

    def test_canRead_plus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("name")

        self.assertEqual(m.canRead(d), True)

    def test_canRead_minus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("canWrite")

        self.assertEqual(m.canRead(d), False)

    def test_canWrite_plus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("name")

        self.assertEqual(m.canWrite(d), True)

    def test_canWrite_minus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("canWrite")

        self.assertEqual(m.canWrite(d), False)

    def test_read_plus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("name")

        self.assertEqual(m.read(d), "asd")

    def test_read_minus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("canWrite")

        self.assertEqual(m.read(d), None)

    def test_write_plus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("name")

        m.write(d, "123")

        self.assertEqual(m.read(d), "123")

    def test_write_minus(self):
        d = MAVariableAccessor("asd")
        m = MAVariableAccessor("canWrite")

        m.write(d, "123")

        self.assertEqual(m.read(d), None)

    def test_getName(self):
        m = MAVariableAccessor("name")

        self.assertEqual(m.name, "name")

    def test_setName(self):
        m = MAVariableAccessor("name")
        m.name = "12345"

        self.assertEqual(m.name, "12345")

    def test_isAbstract(self):
        self.assertEqual(MAVariableAccessor.isAbstract(), False)