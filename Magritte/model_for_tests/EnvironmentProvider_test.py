
from Magritte.model_for_tests.Host import Host
from Magritte.model_for_tests.Account import Account
from Magritte.model_for_tests.Organization import Organization


class TestEnvironmentProvider:
    def __init__(self, num_hosts=3, num_ports_per_host=12, num_accounts=3, num_users=3):
        self._hosts = [Host.random_host(num_ports=num_ports_per_host) for _ in range(num_hosts)]
        self._ports = [port for host in self._hosts for port in host.ports]
        self._accounts = [Account.random_account(self._ports[_]) for _ in range(num_accounts)]
        self._organization = Organization.random_organization(num_users)
        self._users = self._organization.listusers
        self._organization.listcomp = self._hosts
        for user in self._users:
            user.setofaccounts = self._accounts

    @property
    def hosts(self):
        return self._hosts

    @property
    def ports(self):
        return self._ports

    @property
    def accounts(self):
        return self._accounts

    @property
    def organization(self):
        return self._organization

    @property
    def users(self):
        return self._users


def main():
    provider = TestEnvironmentProvider()

    print("Hosts:")
    for host in provider.hosts:
        print(f"IP: {host.ip}")

    print("\nPorts:")
    for port in provider.ports:
        print(f"Host IP: {port.host.ip}, Port Number: {port.numofport}, Status: {port.status}")

    print("\nAccounts:")
    for account in provider.accounts:
        print(f"Login: {account.login}, Password: {account.password}, NTLM: {account.ntlm}, DateOfReg: {account.dateofreg}, Days: {account.days}, Port: {account.port.numofport}")

    print("\nOrganization")
    org = provider.organization
    print(f"Name: {org.name}, Address: {org.address}, Active: {org.active}, ListOfUsers: {org.listnamesofusers}, ListOfComp: {org.listnamesofcomp}")

    print("\nUsers")
    for user in provider.users:
        print(f"RegNum: {user.regnum}, FIO: {user.fio} [{user.organization.name}] - {user.plan}")

if __name__ == "__main__":
    main()

