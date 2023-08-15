from User import User
from Host import Host
import random


class Organization:

    def __init__(self, Name, Address, Active, ListUsers, ListComp):
        assert Name is not None, "Name cannot be None"
        assert Address is not None, "Address cannot be None"
        assert Active is not None, "Active cannot be None"
        assert ListUsers is not None and isinstance(ListUsers, list) and all(
            isinstance(user, User) for user in
            ListUsers), "SetOfAccounts must be a list of Account instances"
        assert ListComp is not None and isinstance(ListComp, list) and all(
            isinstance(comp, Host) for comp in
            ListComp), "SetOfAccounts must be a list of Account instances"

        self._name = Name
        self._address = Address
        self._active = Active
        self._dictusers = ListUsers
        self._dictcomp = ListComp

    @staticmethod
    def generate_name():
        return f'organization{random.randint(1000, 9999)}'

    @staticmethod
    def generate_address():
        block1 = random.randint(0, 255)
        block2 = random.randint(0, 255)
        block3 = random.randint(0, 255)
        block4 = random.randint(0, 255)

        ipAddress = f'{block1}.{block2}.{block3}.{block4}'
        return ipAddress

    @staticmethod
    def generate_active():
        return random.randint(365, 2000)

    @staticmethod
    def generate_listUsers():
        return [User.random_user for _ in range(5)]

    @staticmethod
    def generate_listComps():
        return [Host.random_host() for _ in range(5)]

    @classmethod
    def random_organization(cls, listcomps=Host.random_host()):
        name = cls.generate_name()
        address = cls.generate_address()
        active = cls.generate_active()
        listUsers = cls.generate_listUsers
        listComps = listcomps
        new_organization = cls(name, address, active, listUsers, listComps)
        return new_organization

    def amount_users(self):
        return len(self._dictusers)

    def amount_comp(self):
        return len(self._dictcomp)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, new_active):
        self._active = new_active

    @property
    def listusers(self):
        return self._dictusers

    @listusers.setter
    def listusers(self, new_listusers):
        self._dictusers = new_listusers

    @property
    def listcomp(self):
        return self._dictcomp

    @listcomp.setter
    def listcomp(self, new_listcomp):
        self._dictcomp = new_listcomp
