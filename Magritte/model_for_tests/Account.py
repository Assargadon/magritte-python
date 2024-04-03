
import datetime
import random
from Magritte.MAModel_class import MAModel
from Magritte.model_for_tests.Port import Port


class Account(MAModel):

    def __init__(self):
        self._login = None
        self._password = None
        self._reg_timestamp = None
        self._time = None
        self._port = None
        self._ntlm = ''
        for i in range(32):
            self._ntlm += hex(random.randint(0, 15))[2:]

    @staticmethod
    def generate_login():
        return f'user{random.randint(1, 9999)}'

    @staticmethod
    def generate_password():
        return f'{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}'

    @staticmethod
    def generate_reg_timestamp():
        return datetime.datetime(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))

    @staticmethod
    def generate_days():
        return random.randint(1, 999)

    @classmethod
    def random_account(cls, new_port):
        login = cls.generate_login()
        password = cls.generate_password()
        reg_timestamp = cls.generate_reg_timestamp()
        days = cls.generate_days()
        port = new_port
        new_account = cls()
        new_account.login = login
        new_account.password = password
        new_account.reg_timestamp = reg_timestamp
        new_account.days = days
        new_account.port = port
        return new_account

    def expiration_date(self):
        current_datetime = datetime.datetime.fromtimestamp(self._reg_timestamp)
        date_exp = current_datetime + datetime.timedelta(days=self._time)
        date_exp_timestamp = date_exp.timestamp()

        return datetime.datetime.fromtimestamp(date_exp_timestamp)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, new_login):
        assert new_login is not None, "Login cannot be None"
        self._login = new_login

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        assert new_password is not None, "Password cannot be None"
        self._password = new_password

    @property
    def ntlm(self):
        return self._ntlm

    @ntlm.setter
    def ntlm(self, newNtlm):
        self._ntlm = newNtlm

    @property
    def reg_timestamp(self):
        return self._reg_timestamp

    @reg_timestamp.setter
    def reg_timestamp(self, new_reg_timestamp):
        assert new_reg_timestamp is not None, "Registration timestamp cannot be None"
        self._reg_timestamp = new_reg_timestamp

    @property
    def days(self):
        return self._time

    @days.setter
    def days(self, new_days):
        assert new_days is not None, "Days cannot be None"
        self._time = new_days

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        assert isinstance(new_port, Port), "Expected port to be an instance of Port"
        self._port = new_port
