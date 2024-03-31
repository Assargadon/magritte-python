
import random
from Magritte.MAModel_class import MAModel
from Magritte.model_for_tests.Port import Port

class Host(MAModel):

    def __init__(self):
        self.ip = None
        self.ports = []

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
        new_host = cls()
        ports = [Port.randomPortForHost(new_host) for _ in range(num_ports)]
        new_host.ip = ip
        new_host.ports = ports
        return new_host
