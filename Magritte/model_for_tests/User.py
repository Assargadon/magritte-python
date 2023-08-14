import datetime


class User:

    def __init__(self, RegNum, FIO, DateOfBirth, Gender, organization,
                 DateOfAdmission, DateOfDeparture, SetOfAccounts):
        from Organization import Organization
        from Account import Account

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
        self._organization = Organization
        self._dateofadmission = DateOfAdmission
        self._dateofdeparture = DateOfDeparture
        self._setofaccounts = SetOfAccounts

    def work(self):
        return ((datetime.datetime.strptime(self._dateofdeparture, '%Y-%m-%d')).timestamp() - (datetime.datetime.now()).timestamp()) > 0
