
import datetime
import random
from Magritte.MAModel_class import MAModel
from Magritte.model_for_tests.Port import Port


class Account(MAModel):

    def __init__(self, Login, Password, Dateofreg, Days, port):
        assert isinstance(port, Port), "Expected port to be an instance of Port"
        assert Login is not None, "Login cannot be None"
        assert Password is not None, "Password cannot be None"
        assert Dateofreg is not None, "Dateofreg cannot be None"
        assert Days is not None, "Days cannot be None"

        self._login = Login
        self._password = Password
        self._ntlm = ''
        for i in range(32):
            self._ntlm += hex(random.randint(0, 15))[2:]
        self._dateofreg = Dateofreg.timestamp()
        self._time = Days
        self._port = port

    @staticmethod
    def generate_login():
        return f'user{random.randint(1, 99)}'

    @staticmethod
    def generate_password():
        return f'{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}'

    @staticmethod
    def generate_dateofreg():
        return datetime.datetime(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28))

    @staticmethod
    def generate_days():
        return random.randint(1, 999)

    @classmethod
    def random_account(cls, new_port):
        login = cls.generate_login()
        password = cls.generate_password()
        dateofreg = cls.generate_dateofreg()
        days = cls.generate_days()
        port = new_port
        new_account = cls(login, password, dateofreg, days, port)
        return new_account

    def expiration_date(self):
        current_datetime = datetime.datetime.fromtimestamp(self._dateofreg)
        date_exp = current_datetime + datetime.timedelta(days=self._time)
        date_exp_timestamp = date_exp.timestamp()

        return datetime.datetime.fromtimestamp(date_exp_timestamp)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, new_login):
        self._login = new_login

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    @property
    def ntlm(self):
        return self._ntlm

    @ntlm.setter
    def ntlm(self, newNtlm):
        self._ntlm = newNtlm

    @property
    def dateofreg(self):
        date = datetime.datetime.fromtimestamp(self._dateofreg)
        return date.strftime('%Y-%m-%d')

    @dateofreg.setter
    def dateofreg(self, new_dateofreg):
        self._dateofreg = (datetime.datetime.strptime(new_dateofreg, '%Y-%m-%d')).timestamp()

    @property
    def days(self):
        return self._time

    @days.setter
    def days(self, new_days):
        self._time = new_days

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port
