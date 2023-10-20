from sys import intern

from descriptions.MAMagnitudeDescription_class import MAMagnitudeDescription


def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += self.__class__(label='Minimum', priority=400, accessor=intern('min'))
    desc += self.__class__(label='Maximum', priority=410, accessor=intern('max'))

    return desc
