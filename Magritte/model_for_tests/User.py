from Account import Account
import datetime
import random


class User:

    def __init__(self, RegNum, FIO, DateOfBirth, Gender, organization,
                 DateOfAdmission, DateOfDeparture, SetOfAccounts):
        from Organization import Organization
        assert RegNum is not None, "RegNum cannot be None"
        assert FIO is not None, "FIO cannot be None"
        assert DateOfBirth is not None, "DateOfBirth cannot be None"
        assert Gender is not None, "Gender cannot be None"
        assert isinstance(organization, Organization), "Expected organization to be an instance of Organization"
        assert DateOfAdmission is not None, "DateOfAdmission cannot be None"
        assert DateOfDeparture is not None, "DateOfDeparture cannot be None"
        assert SetOfAccounts is not None and isinstance(SetOfAccounts, list) and all(isinstance(account, Account) for account in SetOfAccounts), "SetOfAccounts must be a list of Account instances"

        self._regnum = RegNum
        self._fio = FIO
        self._dateofbirth = DateOfBirth
        self._gender = Gender
        self._organization = organization
        self._dateofadmission = DateOfAdmission
        self._dateofdeparture = DateOfDeparture
        self._setofaccounts = SetOfAccounts

    @staticmethod
    def generate_regnum():
        return f'user{random.randint(1, 99)}'

    @staticmethod
    def generate_fio():
        return f'default_surname default_name default_patronymic'

    @staticmethod
    def generate_dateofbirth():
        return f'{random.randint(1970, 2004)}-{random.randint(1, 12)}-{random.randint(1, 30)}'

    @staticmethod
    def generate_gender():
        return random.choice(['man', 'woman'])

    @staticmethod
    def generate_organization():
        from Organization import Organization
        return Organization.random_organization()

    @staticmethod
    def generate_dateofadmission():
        return f'{random.randint(2000, 2023)}-{random.randint(1, 12)}-{random.randint(1, 30)}'

    @staticmethod
    def generate_dateofdeparture():
        return f'{random.randint(2000, 2023)}-{random.randint(1, 12)}-{random.randint(1, 30)}'

    @staticmethod
    def generate_setofaccounts():
        return [Account.random_account() for _ in range(5)]

    @classmethod
    def random_user(cls):
        from Organization import Organization
        regnum = cls.generate_regnum()
        fio = cls.generate_fio()
        dateofbirth = cls.generate_dateofbirth()
        gender = cls.generate_gender()
        org = Organization.random_organization()
        dateofadmission = cls.generate_dateofadmission()
        dateofdeparture = cls.generate_dateofdeparture()
        setofacc = cls.generate_setofaccounts()
        new_user = cls(regnum, fio, dateofbirth, gender, org, dateofadmission, dateofdeparture, setofacc)
        return new_user

    def work(self):
        return ((datetime.datetime.strptime(self._dateofdeparture, '%Y-%m-%d')).timestamp() - (datetime.datetime.now()).timestamp()) > 0

    @property
    def regnum(self):
        return self._regnum
    @regnum.setter
    def regnum(self, new_regnum):
        self._regnum = new_regnum

    @property
    def fio(self):
        return self._fio

    @fio.setter
    def fio(self, new_fio):
        self._fio = new_fio

    @property
    def dateofbirth(self):
        return self._dateofbirth

    @dateofbirth.setter
    def dateofbirth(self, new_dateofbirth):
        self._dateofbirth = new_dateofbirth

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        self._gender = new_gender

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, new_organization):
        self._organization = new_organization

    @property
    def dateofadmission(self):
        return self._dateofadmission

    @dateofadmission.setter
    def dateofadmission(self, new_dateofadmission):
        self._dateofadmission = new_dateofadmission

    @property
    def dateofdeparture(self):
        return self._dateofdeparture

    @dateofdeparture.setter
    def dateofdeparture(self, new_dateofdeparture):
        self._dateofdeparture = new_dateofdeparture

    @property
    def setofaccounts(self):
        return self._setofaccounts

    @setofaccounts.setter
    def setofaccounts(self, new_setofaccounts):
        self._setofaccounts = new_setofaccounts
