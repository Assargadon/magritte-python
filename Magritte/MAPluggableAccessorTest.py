from unittest import TestCase
from MAPluggableAccessor_class import MAPluggableAccessor


class MAPluggableAccessorTest(TestCase):

    def test_canRead_plus(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.canRead(d), f_read)

    def test_canRead_minus(self):
        f_read = None

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.canRead(d), None)

    def test_canWrite_plus(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.canWrite(d), f_write)

    def test_canWrite_minus(self):
        f_read = lambda model: model['price'] * model['amount']
        f_write = None

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.canWrite(d), None)

    def test_read(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.read(d), 110)

    def test_write(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        total = 130
        total_accessor.write(d, total)
        self.assertEqual(d['amount'], 13)

    def test_getReadFunc(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.readFunc, f_read)

    def test_setReadFunc(self):
        f_read = lambda model: model['price'] * model['amount']
        f_read2 = lambda model: model

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        total_accessor.readFunc = f_read2
        self.assertEqual(total_accessor.readFunc, f_read2)

    def test_getWriteFunc(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        self.assertEqual(total_accessor.writeFunc, f_write)

    def test_setWriteFunc(self):
        f_read = lambda model: model['price'] * model['amount']

        def f_write(model, value):
            amount = value / model['price']
            model['amount'] = amount

        def f_write2(model, value):
            return value

        total_accessor = MAPluggableAccessor(f_read, f_write)
        d = {'price': 10, 'amount': 11}
        total_accessor.writeFunc = f_write2
        self.assertEqual(total_accessor.writeFunc, f_write2)

    def test_isAbstract(self):
        self.assertEqual(MAPluggableAccessor.isAbstract(), False)
