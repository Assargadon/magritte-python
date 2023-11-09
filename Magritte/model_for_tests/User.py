
from MAModel_class import MAModel
from . Account import Account
import datetime
import random


class User(MAModel):

    def __init__(self, RegNum, FIO, DateOfBirth, Gender, organization,
                 DateOfAdmission, DateOfDeparture, SetOfAccounts):
        from . Organization import Organization
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
        names = ['Danila', 'Ivan', 'Vladimir']
        surnames = ['Smirnov', 'Petrov', 'Ivanov']
        patronymics = ['Ivanovich', 'Petrovich', 'Smirnovich']
        return f'{random.choice(surnames)}, {random.choice(names)}, {random.choice(patronymics)}'

    @staticmethod
    def generate_dateofbirth():
        return datetime.datetime(random.randint(1970, 2004), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_gender():
        return random.choice(['man', 'woman'])

    @staticmethod
    def generate_organization():
        from . Organization import Organization
        return Organization.random_organization()

    @staticmethod
    def generate_dateofadmission():
        return datetime.datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_dateofdeparture():
        return datetime.datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_setofaccounts():
        from . Port import Port
        from . Host import Host
        return [Account.random_account(Port.randomPortForHost(Host.random_host())) for _ in range(5)]

    @classmethod
    def random_user(cls, organization):
        regnum = cls.generate_regnum()
        fio = cls.generate_fio()
        dateofbirth = cls.generate_dateofbirth()
        gender = cls.generate_gender()
        org = organization
        dateofadmission = cls.generate_dateofadmission()
        dateofdeparture = cls.generate_dateofdeparture()
        setofacc = cls.generate_setofaccounts()
        new_user = cls(regnum, fio, dateofbirth, gender, org,  dateofadmission, dateofdeparture, setofacc)
        return new_user

    def work(self):
        return (self._dateofdeparture.timestamp() - (datetime.datetime.now()).timestamp()) > 0

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
        return self._dateofbirth.date()

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
        return self._dateofadmission.date()

    @dateofadmission.setter
    def dateofadmission(self, new_dateofadmission):
        self._dateofadmission = new_dateofadmission

    @property
    def dateofdeparture(self):
        return self._dateofdeparture.date()

    @dateofdeparture.setter
    def dateofdeparture(self, new_dateofdeparture):
        self._dateofdeparture = new_dateofdeparture

    @property
    def setofaccounts(self):
        '''
        logins = []
        for acc in self._setofaccounts:
            logins.append(acc.login)
        return logins
        '''
        return self._setofaccounts

    @setofaccounts.setter
    def setofaccounts(self, new_setofaccounts):
        self._setofaccounts = new_setofaccounts
