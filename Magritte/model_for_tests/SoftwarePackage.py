import random

from Magritte.MAModel_class import MAModel


class SoftwarePackage(MAModel):

    @classmethod
    def softwarePackage(cls, name, version, code):
        p = cls()
        p.name = name
        p.version = version
        p.code = code
        return p

    def __init__(self):
        self.name = None
        self.version = None
        self.code = None

    @staticmethod
    def random_software_package():
        _brands = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]
        _postfix = ["Technology", "Solutions", "Innovations", "Software", "Services", "Systems"]
        _app = ["Database", "Editor", "Compiler", "IDE", "Framework", "Library", "Tool", "Utility", "Application"]
        brand, postfix, app = random.choice(_brands), random.choice(_postfix), random.choice(_app)
        v1, v2, v3 = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
        name = f"{brand} {postfix} {app}"
        version = f"{v1}.{v2}.{v3}"
        code = f"{brand[0]}{postfix[0]}{app[0]}{v1}{v2}{v3}"

        return SoftwarePackage.softwarePackage(name, version, code)

    def __str__(self):
        return f"{self.name} {self.version}"
