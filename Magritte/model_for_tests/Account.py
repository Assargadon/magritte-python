import datetime
import random


class Account:

    def __init__(self, Login, Password, Dateofreg, Days, port):
        from Port import Port
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
