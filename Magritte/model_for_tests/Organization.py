
import random
from Magritte.MAModel_class import MAModel


class Organization(MAModel):

    def __init__(self):
        self._name = None
        self._address = None
        self._active = None
        self._dictusers = []
        self._dictcomp = []

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
        from Magritte.model_for_tests.User import User
        return [User.random_user() for _ in range(5)]

    @staticmethod
    def generate_listComps():
        from Magritte.model_for_tests.Host import Host
        return [Host.random_host() for _ in range(5)]

    @classmethod
    def random_organization(cls, numofsusers=5):
        from Magritte.model_for_tests.User import User
        name = cls.generate_name()
        address = cls.generate_address()
        active = cls.generate_active()
        listComps = cls.generate_listComps()
        new_organization = cls()
        new_organization.name = name
        new_organization.address = address
        new_organization.active = active
        new_organization.listusers = []
        new_organization.listcomp = listComps
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
        assert new_name is not None, "Name cannot be None"
        self._name = new_name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        assert new_address is not None, "Address cannot be None"
        self._address = new_address

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, new_active):
        assert new_active is not None, "Active cannot be None"
        self._active = new_active

    @property
    def listnamesofusers(self):
        return list(map(lambda u: u.regnum, self._dictusers))

    @property
    def listusers(self):
        return self._dictusers

    @listusers.setter
    def listusers(self, new_listusers):
        from Magritte.model_for_tests.User import User
        assert new_listusers is not None and isinstance(new_listusers, list) and all(isinstance(user, User) for user in new_listusers), "ListUsers must be a list of User instances"
        self._dictusers = new_listusers

    @property
    def listnamesofcomp(self):
        return list(map(lambda h: h.ip, self._dictcomp))

    @property
    def listcomp(self):
        return self._dictcomp

    @listcomp.setter
    def listcomp(self, new_listcomp):
        from Magritte.model_for_tests.Host import Host
        assert new_listcomp is not None and isinstance(new_listcomp, list) and all(isinstance(comp, Host) for comp in new_listcomp), "ListComp must be a list of Host instances"
        self._dictcomp = new_listcomp
