from unittest import TestCase
from Magritte.accessors.MAMethodReaderAccessor_class import MAMethodReaderAccessor


class ModelWithReadMethod:

    def __init__(self, aValue):
        self.value = aValue

    def ReadMethod(self):
        return self.value

class ModelUnreadable:
    pass

readMethodName = "ReadMethod";

class ModelWithConsonantField:
    def __init__(self):
        #self.ReadMethod = 777
        setattr(self, readMethodName, 777)

class MAMethodReaderAccessorTest(TestCase):

    def setUp(self):
        self.value = 10
        self.model                = ModelWithReadMethod(self.value)
        self.model_without_method = ModelUnreadable()
        self.model_with_consonant = ModelWithConsonantField()
        self.accessor          = MAMethodReaderAccessor(readMethodName)#"ReadMethod")
        self.wrongNameAccessor = MAMethodReaderAccessor("blah-blah")

    def test_canRead(self):
        self.assertEqual(self.accessor         .canRead(self.model               ), True)
        self.assertEqual(self.wrongNameAccessor.canRead(self.model               ), False)

        self.assertEqual(self.accessor         .canRead(self.model_without_method), False)
        self.assertEqual(self.accessor         .canRead(self.model_with_consonant), False)

    def test_canWrite(self):
        self.assertEqual(self.accessor.canWrite(self.model), False)

    def test_read(self):
        self.assertEqual(
            self.accessor                  .read(self.model), self.value)
        with self.assertRaises(Exception):
            self.wrongNameAccessor         .read(self.model)
        with self.assertRaises(Exception):
            self.accessor                  .read(self.model_without_method)
        with self.assertRaises(Exception):
            self.accessor                  .read(self.model_with_consonant)

    def test_write(self):
        self.accessor.write(self.model, 0) # just make shure it doestn't crash

