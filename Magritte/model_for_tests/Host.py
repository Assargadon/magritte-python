
import random
from Magritte.MAModel_class import MAModel
from Magritte.model_for_tests.Port import Port
from Magritte.model_for_tests.SoftwarePackage import SoftwarePackage


class Host(MAModel):

    _taken_ips = set()

    def __init__(self):
        self._ip = None
        self._ports = []
        self._software = []

    @staticmethod
    def generate_ip():
        block1 = random.randint(0, 255)
        block2 = random.randint(0, 255)
        block3 = random.randint(0, 255)
        block4 = random.randint(0, 255)

        while f'{block1}.{block2}.{block3}.{block4}' in Host._taken_ips:
            block1 = random.randint(0, 255)
            block2 = random.randint(0, 255)
            block3 = random.randint(0, 255)
            block4 = random.randint(0, 255)

        ipAddress = f'{block1}.{block2}.{block3}.{block4}'
        Host._taken_ips.add(ipAddress)

        return ipAddress

    @classmethod
    def random_host(cls, num_ports=12):
        ip = cls.generate_ip()
        new_host = cls()
        ports = [Port.randomPortForHost(new_host) for _ in range(num_ports)]
        software = [SoftwarePackage.random_software_package() for _ in range(3)]
        new_host._ip = ip
        new_host._ports = ports
        new_host._software = software
        return new_host

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, newIP):
        self._ip = newIP

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, newPorts):
        self._ports = newPorts

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, newSoftware):
        self._software = newSoftware
