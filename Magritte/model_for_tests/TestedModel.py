import datetime
import random


class User:

    def __init__(self, RegNum, FIO, DateOfBirth, Gender, Organization,
                 DateOfAdmission, DateOfDeparture, SetOfAccounts):
        self._regnum = RegNum
        self._fio = FIO
        self._dateofbirth = DateOfBirth
        self._gender = Gender
        self._organization = Organization
        self._dateofadmission = DateOfAdmission
        self._dateofdeparture = DateOfDeparture
        self._setofaccounts = SetOfAccounts

    def work(self):
        return ((datetime.datetime.strptime(self._dateofdeparture, '%Y-%m-%d')).timestamp() - (datetime.datetime.now()).timestamp()) > 0


class Organization:

    def __init__(self, Name, Address, Active, ListUsers, ListComp):
        self._name = Name
        self._address = Address
        self._active = Active
        self._dictusers = ListUsers
        self._dictcomp = ListComp

    def amount_users(self):
        return len(self._dictusers)

    def amount_comp(self):
        return len(self._dictcomp)


class Account:

    def __init__(self, Login, Password, Dateofreg, Days, Port):
        self._login = Login
        self._password = Password
        self._ntlm = ''
        for i in range(32):
            self._ntlm += hex(random.randint(0, 15))[2:]
        self._dateofreg = (datetime.datetime.strptime(Dateofreg, '%Y-%m-%d')).timestamp()
        self._time = Days
        self._port = Port

    def expiration_date(self):
        current_datetime = datetime.datetime.fromtimestamp(self._dateofreg)
        date_exp = current_datetime + datetime.timedelta(days=self._time)
        date_exp_timestamp = date_exp.timestamp()

        return datetime.datetime.fromtimestamp(date_exp_timestamp)

    @property
    def ntlm(self):
        return self._ntlm

    @ntlm.setter
    def ntlm(self, newNtlm):
        self._ntlm = newNtlm
