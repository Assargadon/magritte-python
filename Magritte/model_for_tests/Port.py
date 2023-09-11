
from MAModel_class import MAModel
import random

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

    def __init__(self, host, numofport=None):
        from . Host import Host
        assert isinstance(host, Host), "Expected host to be an instance of Host"
        assert numofport is not None, "numofport cannot be None"
        
        self._host = host
        self._numofport = numofport

    @staticmethod
    def generate_numofport():
        return random.choice(Port.COMMON_PORTS)

    @classmethod
    def randomPortForHost(cls, host):
        return cls(host, cls.generate_numofport())

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
