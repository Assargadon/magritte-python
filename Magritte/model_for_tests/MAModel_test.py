from unittest import TestCase
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from .User import User


class MAModelTest(TestCase):

    def setUp(self):
        self.model = User(User.generate_regnum(), User.generate_fio(), User.generate_dateofbirth(), User.generate_gender(), User.generate_organization(),
                 User.generate_dateofadmission(), User.generate_dateofdeparture(), User.generate_setofaccounts())
        self.fioDesc = MAStringDescription()
        self.fioDesc.accessor = MAAttrAccessor('fio')
       
    def test_write_read(self):
        self.model.writeUsing(description = self.fioDesc, value = "goodok")
       
        self.assertEqual(self.model.readUsing(self.fioDesc), "goodok")
