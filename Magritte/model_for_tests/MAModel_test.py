from unittest import TestCase
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from .User import User


class MAModelTest(TestCase):

    def setUp(self):
        new_user = User()
        self.model = new_user
        new_user.regnum = User.generate_regnum()
        new_user.fio = User.generate_fio()
        new_user.dateofbirth = User.generate_dateofbirth()
        new_user.gender = User.generate_gender()
        new_user.organization = User.generate_organization()
        new_user.dateofadmission = User.generate_dateofadmission()
        new_user.dateofdeparture = User.generate_dateofdeparture()
        new_user.setofaccounts = User.generate_setofaccounts()
        self.fioDesc = MAStringDescription()
        self.fioDesc.accessor = MAAttrAccessor('fio')
       
    def test_write_read(self):
        self.model.writeUsing(description = self.fioDesc, value = "goodok")
       
        self.assertEqual(self.model.readUsing(self.fioDesc), "goodok")
