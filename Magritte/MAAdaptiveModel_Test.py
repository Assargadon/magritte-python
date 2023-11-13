from unittest import TestCase
from MAAdaptiveModel_class import MAAdaptiveModel
from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MANumberDescription_class import MANumberDescription
from errors.MAReadError import MAReadError
from errors.MAWriteError import MAWriteError


class MAAdaptiveModelTest(TestCase):

    def setUp(self):
        self.nameDesc = MAStringDescription()
        self.surnameDesc = MAStringDescription()
        self.ageDesc = MANumberDescription()

        self.adaptiveModel = MAAdaptiveModel()        
        self.adaptiveModel.magritteDescription += self.nameDesc 
        self.adaptiveModel.magritteDescription += self.surnameDesc
        self.adaptiveModel.magritteDescription += self.ageDesc
        
    def test_write_read(self):
        self.adaptiveModel.writeUsing(description = self.nameDesc, value = "goodok")
        self.adaptiveModel.writeUsing(description = self.surnameDesc, value = "assargadonov")
        self.adaptiveModel.writeUsing(description = self.ageDesc, value = 40)
        
        self.assertEqual(self.adaptiveModel.readUsing(self.nameDesc), "goodok")
        self.assertEqual(self.adaptiveModel.readUsing(self.surnameDesc), "assargadonov")
        self.assertEqual(self.adaptiveModel.readUsing(self.ageDesc), 40)

    def test_read_uninitialized(self):
        self.assertIsNone(self.adaptiveModel.readUsing(self.nameDesc))
        self.assertIsNone(self.adaptiveModel.readUsing(self.surnameDesc))
        self.assertIsNone(self.adaptiveModel.readUsing(self.ageDesc))

    def test_access_undescribed(self):
        notFieldOfAdaptiveModel = MAStringDescription()

        with self.assertRaises(MAReadError):
            self.adaptiveModel.readUsing(notFieldOfAdaptiveModel)

        with self.assertRaises(MAWriteError):
            self.adaptiveModel.writeUsing(notFieldOfAdaptiveModel, "some value")
