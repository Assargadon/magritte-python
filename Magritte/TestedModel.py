import datetime
import random


class Host:

    def __init__(self):
        self._ip = self.generate_ip()
        self._ports = [20, 21, 22, 23, 25, 42, 43, 53, 67, 69, 80, 110, 115, 123,
                       137, 138, 139, 143, 161, 179, 443, 445, 514, 515, 993, 995,
                       1080, 1194, 1433, 1702, 1723, 3128, 3268, 3306, 3389, 5432,
                       5060, 5900, 5938, 8080, 10000, 20000]

    def generate_ip(self):
        block1 = random.randint(0, 255)
        block2 = random.randint(0, 255)
        block3 = random.randint(0, 255)
        block4 = random.randint(0, 255)

        ipAddress = f'{block1}.{block2}.{block3}.{block4}'
        return ipAddress

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, newIP):
        self._ip = newIP

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, newPorts):
        self._ports = newPorts


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
        return self._dateofdeparture != None


class Organization:

    def __init__(self, Name, Address, Active, DictUsers, DictComp):
        self._name = Name
        self._address = Address
        self._active = Active
        self._dictusers = DictUsers
        self._dictcomp = DictComp

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

