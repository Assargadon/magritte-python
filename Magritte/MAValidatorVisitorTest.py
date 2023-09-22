
from unittest import TestCase
from MAModel_class import MAModel
from MAContainer_class import MAContainer
from accessors.MAAttrAccessor_class import MAAttrAccessor
from MACondition import MACondition
from MAStringDescription_class import MAStringDescription
from MAIntDescription_class import MAIntDescription
from MAToOneRelationDescription_class import MAToOneRelationDescription
from MAToManyRelationDescription_class import MAToManyRelationDescription
from MAValidatorVisitor_class import MAValidatorVisitor
from accessors.MADictAccessor_class import MADictAccessor

class _ValidatorTestModel(MAModel):
    str_value = None
    int_value = 36


class MAToOneRelationDescriptionTest(TestCase):

    def setUp(self):
        self.model = _ValidatorTestModel()
        self.visitor = MAValidatorVisitor()

        self.desc_good1 = MAContainer()
        self.desc_good1 += MAStringDescription(label='String value', required=False, accessor=MAAttrAccessor(aAttrName='str_value'))
        self.desc_good1 += MAIntDescription(label='Int value', required=False, conditions=[(MACondition.model >= 5, '>=5')], accessor=MAAttrAccessor(aAttrName='int_value'))

        self.desc_good2 = MAContainer()
        self.desc_good2 += MAStringDescription(label='String value', required=False, accessor=MAAttrAccessor(aAttrName='str_value'))
        self.desc_good2 += MAIntDescription(label='Int value', required=True, conditions=[(MACondition.model <= 100, '<=100')], accessor=MAAttrAccessor(aAttrName='int_value'))

        self.desc_wrong1 = MAContainer()
        self.desc_wrong1 += MAStringDescription(label='Nonexistent value', required=True, accessor=MAAttrAccessor(aAttrName='no_value'))
        self.desc_wrong1 += MAIntDescription(label='Int value', required=False, accessor=MAAttrAccessor(aAttrName='int_value'))

        self.desc_wrong2 = MAContainer()
        self.desc_wrong2 += MAStringDescription(label='String value', required=False, accessor=MAAttrAccessor(aAttrName='str_value'))
        self.desc_wrong2 += MAIntDescription(label='Int value', required=True, conditions=[(MACondition.model == 98, '==98')], accessor=MAAttrAccessor(aAttrName='int_value'))

        self.desc_wrong3 = MAContainer()
        self.desc_wrong3 += MAStringDescription(label='String value', required=True, accessor=MAAttrAccessor(aAttrName='str_value'))


    def testValidator_desc_good1(self):
        self.assertEqual(len(self.visitor.validateModelDescription(self.model, self.desc_good1)), 0, "Good description should not produce validation errors")

    def testValidator_desc_good2(self):
        self.assertEqual(len(self.visitor.validateModelDescription(self.model, self.desc_good2)), 0, "Good description should not produce validation errors")

    def testValidator_desc_wrong1(self):
        self.assertNotEqual(len(self.visitor.validateModelDescription(self.model, self.desc_wrong1)), 0, "Wrong description should produce validation errors")

    def testValidator_desc_wrong2(self):
        self.assertNotEqual(len(self.visitor.validateModelDescription(self.model, self.desc_wrong2)), 0, "Wrong description should produce validation errors")

    def testValidator_desc_wrong3(self):
        self.assertNotEqual(len(self.visitor.validateModelDescription(self.model, self.desc_wrong3)), 0, "Wrong description should produce validation errors")

    def isSatisfiedBy(self, description, model):
        return len(description.validate(model)) == 0

    def test_optionalContainer(self):
        optionalContainer = MAContainer(required = False)
        self.assertTrue(self.isSatisfiedBy(optionalContainer, None), "None is valid value for optional MAContainer")

        mandatoryContainer = MAContainer(required = True)
        self.assertFalse(self.isSatisfiedBy(mandatoryContainer, None), "None is NOT valid value for non-optional/mandatored MAContainer")
        
    def test_toManyValidation(self):
        
        class TestArrayHolder(MAModel):
            def __init__(self, array):
                self.arr = array
        
        desc = MAContainer()
        desc += MAToManyRelationDescription(accessor = "arr", reference = self.desc_good1, classes=[_ValidatorTestModel], required = False)
        
        self.assertTrue(self.isSatisfiedBy(desc, TestArrayHolder([])), "Empty array do not holds elements to broke reference description validation")
        self.assertTrue(self.isSatisfiedBy(desc, TestArrayHolder([self.model])))

    def test_toOneValidation(self):

        class TestObjectHolder(MAModel):
            def __init__(self, obj):
                self.obj = obj

        desc = MAContainer()
        desc += MAToOneRelationDescription(accessor = "obj", reference = self.desc_good1, classes=[_ValidatorTestModel], required = False)
        
        self.assertTrue(self.isSatisfiedBy(desc, TestObjectHolder(None)), "None is OK for optional field")
        self.assertTrue(self.isSatisfiedBy(desc, TestObjectHolder(self.model)))

    def test_multipleErrors(self):
        desc = MAContainer()
        desc += MAStringDescription(accessor = MADictAccessor("str"), required = True)
        desc += MAIntDescription(accessor = MADictAccessor("int"), required = True, min = 13, max = 66 )
        
        self.assertEqual(len(desc.validate({"str": "Test", "int": 20})), 0)
        self.assertEqual(len(desc.validate({"str": "Test", "int": 100})), 1)
        self.assertEqual(len(desc.validate({"str": None, "int": None})), 2)
        self.assertEqual(len(desc.validate({"str": None, "int": 100})), 2)
