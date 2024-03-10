
import datetime
import random
from Magritte.MAModel_class import MAModel
from Magritte.model_for_tests.Account import Account


class User(MAModel):

    def __init__(self):
        self._regnum = None
        self._fio = None
        self._dateofbirth = None
        self._gender = None
        self._organization = None
        self._dateofadmission = None
        self._dateofdeparture = None
        self._setofaccounts = []
        self.plan = None

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
        return datetime.date(random.randint(1970, 2004), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_gender():
        return random.choice(['man', 'woman'])

    @staticmethod
    def generate_organization():
        from Magritte.model_for_tests.Organization import Organization
        return Organization.random_organization()

    @staticmethod
    def generate_dateofadmission():
        return datetime.date(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_dateofdeparture():
    # in half of the cases, the user will not have a date of departure
        if random.random() < 0.5:
            return None
        else:
            return datetime.date(random.randint(2022, 2025), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_setofaccounts():
        from Magritte.model_for_tests.Port import Port
        from Magritte.model_for_tests.Host import Host
        return [Account.random_account(Port.randomPortForHost(Host.random_host())) for _ in range(5)]

    @staticmethod
    def generate_subscription_plan():
        from Magritte.model_for_tests.SubscriptionPlan import SubscriptionPlan
        if random.random() < 0.5:
            return SubscriptionPlan.entries[0]
        else: #select a random non-free plan
            return random.choice(SubscriptionPlan.entries[1:])

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
        new_user = cls()
        new_user.regnum = regnum
        new_user.fio = fio
        new_user.dateofbirth = dateofbirth
        new_user.gender = gender
        new_user.organization = org
        new_user.dateofadmission = dateofadmission
        new_user.dateofdeparture = dateofdeparture
        new_user.setofaccounts = setofacc
        new_user.plan = cls.generate_subscription_plan()
        return new_user

    def is_works_now(self):
        if self.dateofdeparture is None:
            return self.dateofadmission <= datetime.date.today()
        else:
            return self.dateofadmission <= datetime.date.today() <= self.dateofdeparture

    @property
    def regnum(self):
        return self._regnum

    @regnum.setter
    def regnum(self, new_regnum):
        assert new_regnum is not None, "RegNum cannot be None"
        self._regnum = new_regnum

    @property
    def fio(self):
        return self._fio

    @fio.setter
    def fio(self, new_fio):
        assert new_fio is not None, "FIO cannot be None"
        self._fio = new_fio

    @property
    def dateofbirth(self):
        return self._dateofbirth

    @dateofbirth.setter
    def dateofbirth(self, new_dateofbirth):
        assert new_dateofbirth is not None, "DateOfBirth cannot be None"
        self._dateofbirth = new_dateofbirth

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        assert new_gender is not None, "Gender cannot be None"
        self._gender = new_gender

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, new_organization):
        from Magritte.model_for_tests.Organization import Organization
        assert isinstance(new_organization, Organization), "Expected organization to be an instance of Organization"
        self._organization = new_organization

    @property
    def dateofadmission(self):
        return self._dateofadmission

    @dateofadmission.setter
    def dateofadmission(self, new_dateofadmission):
        assert new_dateofadmission is not None, "DateOfAdmission cannot be None"
        self._dateofadmission = new_dateofadmission

    @property
    def dateofdeparture(self):
        return self._dateofdeparture

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
        assert new_setofaccounts is not None and isinstance(new_setofaccounts, list) and all(isinstance(account, Account) for account in new_setofaccounts), "SetOfAccounts must be a list of Account instances"
        self._setofaccounts = new_setofaccounts
