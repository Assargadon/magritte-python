
import random
from Magritte.MAModel_class import MAModel

class Port(MAModel):
    COMMON_PORTS = [20,  # FTP
                   22,  # SSH
                   25,  # SMTP
                   53,  # DNS
                   80,  # HTTP
                   110, # POP3
                   143, # IMAP
                   443, # HTTPS
                   465, # SMTPS
                   587, # SMTP TLS/SSL
                   993, # IMAPS
                   995] # POP3S

    def __init__(self):
        from Magritte.model_for_tests.Host import Host
        self._host = None
        self._numofport = None

    @staticmethod
    def generate_numofport():
        return random.choice(Port.COMMON_PORTS)

    @classmethod
    def randomPortForHost(cls, host):
        new_port = cls()
        new_port._host = host
        new_port._numofport = cls.generate_numofport()
        return new_port

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, new_host):
        self._host = new_host

    @property
    def numofport(self):
        return self._numofport

    @numofport.setter
    def numofport(self, new_numofport):
        self._numofport = new_numofport
