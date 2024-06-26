
from unittest import TestCase
from Magritte.MAModel_class import MAModel
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.MACondition import MACondition
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.visitors.MAValidatorVisitor_class import MAValidatorVisitor
from Magritte.accessors.MADictAccessor_class import MADictAccessor

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
        desc += MAToManyRelationDescription(accessor = "arr", reference = self.desc_good1, required = False)
        
        self.assertTrue(self.isSatisfiedBy(desc, TestArrayHolder([])), "Empty array do not holds elements to broke reference description validation")
        self.assertTrue(self.isSatisfiedBy(desc, TestArrayHolder([self.model])))

    def test_toOneValidation(self):

        class TestObjectHolder(MAModel):
            def __init__(self, obj):
                self.obj = obj

        desc = MAContainer()
        desc += MAToOneRelationDescription(accessor = "obj", reference = self.desc_good1, required = False)
        
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

    def test_multipleErrorsByMultipleConditions(self):
        desc = MAIntDescription(
            min = 2,
            max = 10,
            conditions = [
                MACondition.model != 0,
                lambda x: x % 2 == 1 #should be odd
            ]
        )
        
        self.assertEqual(len(desc.validate(3)), 0)
        self.assertEqual(len(desc.validate(1)), 1) # less than min
        self.assertEqual(len(desc.validate(4)), 1) # even
        self.assertEqual(len(desc.validate(12)), 2) # even, more than max
        self.assertEqual(len(desc.validate(0)), 3) # even, less than min, equal to zero
