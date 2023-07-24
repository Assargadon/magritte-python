from unittest import TestCase
from Magritte.MADescription_class import MADescription
from MANullAccessor_class import MANullAccessor


class MADescriptionTest(TestCase):

    def setUp(self):
        self.inst1 = MADescription()
        self.inst2 = MADescription()
        self.inst3 = MADescription()
        self.inst1['accessor'] = 3
        self.inst2['kindErrorMessage'] = 3
        self.accessorTrue = 'accessor'
        self.accessorFalse = 3

    def test_eq(self):
        self.assertEqual(self.inst1 == self.inst1, True)
        self.assertEqual(self.inst1 == self.inst2, False)

    def test_setitem_and_getitem(self):
        self.assertEqual(self.inst1['accessor'], 3)

    def test_contains(self):
        self.assertEqual(self.inst1.__contains__(self.accessorTrue), True)
        self.assertEqual(self.inst1.__contains__(self.accessorFalse), False)

    def test_get(self):
        self.assertEqual(self.inst1.get('accessor', 0), 3)
        self.assertEqual(self.inst1.get('property', 0), 0)

    def test_isAbstract(self):
        self.assertEqual(self.inst1.isAbstract(), True)

    def test_getAccessor(self):
        self.assertEqual(isinstance(self.inst3.accessor, MANullAccessor), True)

    def test_setAccessor(self):
        self.inst1.accessor = 3
        self.assertEqual(self.inst1.accessor, 3)

    def test_getKind(self):
        self.assertEqual(isinstance(self.inst3.kind, object), True)

    def test_setKind(self):
        self.inst1.kind = 123
        self.assertEqual(self.inst1.kind, 123)

    def test_isKindDefined(self):
        self.inst1.kind = 123
        self.assertEqual(self.inst1.isKindDefined(), True)
        self.assertEqual(self.inst2.isKindDefined(), False)

    def test_getKindErrorMessage(self):
        self.assertEqual(self.inst1.kindErrorMessage, 'Invalid input given')

    def test_setKindErrorMessage(self):
        self.inst1.kindErrorMessage = 'error'
        self.assertEqual(self.inst1.kindErrorMessage, 'error')

    def test_getReadOnly(self):
        self.assertEqual(self.inst1.readOnly, False)

    def test_setReadOnly(self):
        self.inst1.readOnly = True
        self.assertEqual(self.inst1.readOnly, True)

    def test_isReadOnly(self):
        self.inst1.readOnly = True
        self.assertEqual(self.inst1.isReadOnly(), True)
        self.assertEqual(self.inst2.isReadOnly(), False)

    def test_beReadOnly(self):
        self.inst1.beReadOnly()
        self.assertEqual(self.inst1.readOnly, True)

    def test_beWriteable(self):
        self.inst1.beWriteable()
        self.assertEqual(self.inst1.readOnly, False)

    def test_getRequired(self):
        self.assertEqual(self.inst1.required, False)

    def test_setRequired(self):
        self.inst1.required = True
        self.assertEqual(self.inst1.required, True)

    def test_isRequired(self):
        self.inst1.required = True
        self.assertEqual(self.inst1.isRequired(), True)
        self.assertEqual(self.inst2.isRequired(), False)

    def test_beRequired(self):
        self.inst1.beRequired()
        self.assertEqual(self.inst1.required, True)

    def test_beOptional(self):
        self.inst1.beOptional()
        self.assertEqual(self.inst1.required, False)

    def test_getDefault(self):
        self.assertEqual(self.inst1.default, None)

    def test_setDefault(self):
        df = self.inst1.default
        self.inst1.default = 1
        self.assertEqual(self.inst1.default, None)

    def test_getUndefinedValue(self):
        self.assertEqual(self.inst1.undefinedValue, None)

    def test_setUndefinedValue(self):
        self.inst1.undefinedValue = 123
        self.assertEqual(self.inst1.undefinedValue, 123)

    def test_getName(self):
        self.assertEqual(self.inst1.name, None)

    def test_setName(self):
        self.inst1.name = 'Evedg'
        self.assertEqual(self.inst1.name, 'Evedg')

    def test_getComment(self):
        self.assertEqual(self.inst1.name, None)

    def test_setComment(self):
        self.inst1.comment = 'comment'
        self.assertEqual(self.inst1.comment, 'comment')

    def test_hasComment(self):
        self.assertEqual(self.inst1.hasComment(), False)
        self.inst1.comment = 'comment'
        self.assertEqual(self.inst1.hasComment(), True)

    def test_getGroup(self):
        self.assertEqual(self.inst1.group, None)

    def test_setGroup(self):
        self.inst1.group = 'group'
        self.assertEqual(self.inst1.group, 'group')

    def test_getLabel(self):
        self.assertEqual(self.inst1.label, '')

    def test_setLabel(self):
        self.inst1.label = 'label'
        self.assertEqual(self.inst1.label, 'label')

    def test_hasLabel(self):
        self.assertEqual(self.inst1.hasLabel(), False)
        self.inst1.label = 'label'
        self.assertEqual(self.inst1.hasLabel(), True)

    def test_getPriority(self):
        self.assertEqual(self.inst1.priority, 0)

    def test_setPriority(self):
        self.inst1.priority = 1
        self.assertEqual(self.inst1.priority, 1)

    def test_getVisible(self):
        self.assertEqual(self.inst1.visible, True)

    def test_setVisible(self):
        self.inst1.visible = False
        self.assertEqual(self.inst1.visible, False)

    def test_isVisible(self):
        self.assertEqual(self.inst1.isVisible(), False)
        self.inst1.readOnly = True
        self.assertEqual(self.inst1.isVisible(), True)

    def test_beVisible(self):
        self.inst1.beVisible()
        self.assertEqual(self.inst1.isVisible(), True)

    def test_beHidden(self):
        self.inst1.beHidden()
        self.assertEqual(self.inst1.isVisible(), False)

    def test_getUndefined(self):
        self.assertEqual(self.inst1.undefined, '')

    def test_setUndefined(self):
        self.inst1.undefined = 'str'
        self.assertEqual(self.inst1.undefined, 'str')

    def test_isSortable(self):
        self.assertEqual(self.inst1.isSortable(), False)
