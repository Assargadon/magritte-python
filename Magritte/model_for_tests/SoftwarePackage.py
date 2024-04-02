import random

from Magritte.MAModel_class import MAModel


class SoftwarePackage(MAModel):

    @classmethod
    def softwarePackage(cls, name, version):
        p = cls()
        p.name = name
        p.version = version
        return p

    def __init__(self):
        self.name = None
        self.version = None

    @staticmethod
    def random_software_package():
        _brands = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
        _postfix = ["Technology", "Solutions", "Innovations", "Software", "Services", "Systems"]
        _app = ["Database", "Editor", "Compiler", "IDE", "Framework", "Library", "Tool", "Utility", "Application"]
        name = f"{random.choice(_brands)} {random.choice(_postfix)} {random.choice(_app)}"
        version = f"{random.randint(0, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}"

        return SoftwarePackage.softwarePackage(name, version)

    def __str__(self):
        return f"{self.name} {self.version}"
