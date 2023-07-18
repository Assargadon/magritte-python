import datetime
import random


class Host:

    def __init__(self, IP):
        if IP is not None:
            self._ip = IP
        else:
            self._ip = self.generate_ip()
        self._ports = [Port('Name1', 20), Port('Name2', 21), Port('Name3', 22), Port('Name4', 23),
                       Port('Name5', 25), Port('Name6', 42), Port('Name7', 43), Port('Name8', 53),
                       Port('Name9', 67), Port('Name10', 69), Port('Name11', 80), Port('Name12', 110),
                       Port('Name13', 115), Port('Name14', 123), Port('Name15', 137), Port('Name16', 138),
                       Port('Name17', 139), Port('Name18', 143), Port('Name19', 161), Port('Name20', 179),
                       Port('Name21', 443), Port('Name22', 445), Port('Name23', 514), Port('Name24', 515),
                       Port('Name25', 993), Port('Name26', 995), Port('Name27', 1080), Port('Name28', 1194),
                       Port('Name29', 1433), Port('Name30', 1702), Port('Name31', 1723), Port('Name32', 3128),
                       Port('Name33', 3268), Port('Name34', 3306), Port('Name35', 3389), Port('Name36', 5432),
                       Port('Name37', 5060), Port('Name38', 5900), Port('Name39', 5938), Port('Name40', 8080),
                       Port('Name41', 10000), Port('Name42', 20000)]

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

class Port:

    def __init__(self, Host, NumOfPort):
        self._host = Host
        if NumOfPort is not None:
            self._numofport = NumOfPort
        else:
            self._numofport = Host.ports[random.randint(0, 41)]

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, newHost):
        self._host = newHost

    @property
    def numofport(self):
        return self._numofport

    @numofport.setter
    def numofport(self, newNumofports):
        self._numofport = newNumofports


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
