from Host import Host
from Port import Port
from Account import Account

class TestEnvironmentProvider:
    def __init__(self, num_hosts=3, num_ports_per_host=12, num_accounts=3):
        self._hosts = [Host.random_host(num_ports=num_ports_per_host) for _ in range(num_hosts)]
        self._ports = [port for host in self._hosts for port in host.ports]
        self._accounts = [Account.random_account() for _ in range(num_accounts)]

    @property
    def hosts(self):
        return self._hosts

    @property
    def ports(self):
        return self._ports

    @property
    def accounts(self):
        return self._accounts


def main():
    provider = TestEnvironmentProvider()

    print("Hosts:")
    for host in provider.hosts:
        print(f"IP: {host.ip}")

    print("\nPorts:")
    for port in provider.ports:
        print(f"Host IP: {port.host.ip}, Port Number: {port.numofport}")

    print("\nAccounts:")
    for account in provider.accounts:
        print(f"Login: {account.login}, Password: {account.password}, NTLM: {account.ntlm}, DateOfReg: {account.dateofreg}, Days: {account.days}, Port: {account.port.numofport}")

if __name__ == "__main__":
    main()

