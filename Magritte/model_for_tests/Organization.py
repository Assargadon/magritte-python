class Organization:

    def __init__(self, Name, Address, Active, ListUsers, ListComp):
        from User import User
        from Host import Host
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

    def amount_users(self):
        return len(self._dictusers)

    def amount_comp(self):
        return len(self._dictcomp)