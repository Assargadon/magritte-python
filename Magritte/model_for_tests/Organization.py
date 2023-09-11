
from MAModel_class import MAModel
import random


class Organization(MAModel):

    def __init__(self, Name, Address, Active, ListUsers, ListComp):
        from . User import User
        from . Host import Host
        assert Name is not None, "Name cannot be None"
        assert Address is not None, "Address cannot be None"
        assert Active is not None, "Active cannot be None"
        assert ListUsers is not None and isinstance(ListUsers, list) and all(
            isinstance(user, User) for user in
            ListUsers), "ListUsers must be a list of User instances"
        assert ListComp is not None and isinstance(ListComp, list) and all(
            isinstance(comp, Host) for comp in
            ListComp), "ListComp must be a list of Host instances"

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
        return f'address{random.randint(1000, 9999)}'

    @staticmethod
    def generate_active():
        return random.choice([False, True])

    @staticmethod
    def generate_listUsers():
        from User import User
        return [User.random_user() for _ in range(5)]

    @staticmethod
    def generate_listComps():
        from . Host import Host
        return [Host.random_host() for _ in range(5)]

    @classmethod
    def random_organization(cls, numofsusers=5):
        from . User import User
        name = cls.generate_name()
        address = cls.generate_address()
        active = cls.generate_active()
        listComps = cls.generate_listComps()
        new_organization = cls(name, address, active, [], listComps)
        listUsers = [User.random_user(new_organization) for _ in range(numofsusers)]
        new_organization._dictusers = listUsers
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
    def listnamesofusers(self):
        return list(map(lambda u: u.regnum, self._dictusers))

    @property
    def listusers(self):
        return self._dictusers

    @listusers.setter
    def listusers(self, new_listusers):
        self._dictusers = new_listusers

    @property
    def listnamesofcomp(self):
        return list(map(lambda h: h.ip, self._dictcomp))

    @property
    def listcomp(self):
        return self._dictcomp

    @listcomp.setter
    def listcomp(self, new_listcomp):
        self._dictcomp = new_listcomp
