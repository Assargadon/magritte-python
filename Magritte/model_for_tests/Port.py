
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

    STATUSES = ["open", "closed", "filtered"]

    def __init__(self):
        from Magritte.model_for_tests.Host import Host
        self._host = None
        self._numofport = None
        self._status = None
        self._id = None

    @staticmethod
    def generate_numofport():
        if random.random() < 0.7:
            return random.choice(Port.COMMON_PORTS)
        else:
            return random.randint(1025, 65535)

    def generate_status(self):
        if self._numofport in Port.COMMON_PORTS:
            if self._numofport % 2 == 0:
                return "open"
            else:
                return "filtered"
        else:
            return random.choice(Port.STATUSES)

    @classmethod
    def randomPortForHost(cls, host):
        new_port = cls()
        new_port._host = host
        new_port._numofport = cls.generate_numofport()
        new_port._status = new_port.generate_status()
        return new_port

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

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

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status not in Port.STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        self._status = new_status

    @property
    def label(self):
        return f"{self.host.ip}:{self.numofport}"
