import random
from Port import Port

class Host:

    def __init__(self, IP, ports):
        assert IP is not None, "IP cannot be None"
        assert ports is not None and isinstance(ports, list) and all(isinstance(port, Port) for port in ports), \
            "ports must be a list of Port instances"
        
        self._ip = IP
        self._ports = ports

    @staticmethod
    def generate_ip():
        block1 = random.randint(0, 255)
        block2 = random.randint(0, 255)
        block3 = random.randint(0, 255)
        block4 = random.randint(0, 255)

        ipAddress = f'{block1}.{block2}.{block3}.{block4}'
        return ipAddress

    @classmethod
    def random_host(cls, num_ports=12):
        ip = cls.generate_ip()
        new_host = cls(ip, [])
        ports = [Port.randomPortForHost(new_host) for _ in range(num_ports)]
        new_host._ports = ports
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
