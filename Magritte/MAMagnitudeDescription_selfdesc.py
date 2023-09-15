from accessors.MAAttrAccessor_class import MAAttrAccessor
from MAMagnitudeDescription_class import MAMagnitudeDescription

def magritteDescription(self, parentDescription):
    desc = parentDescription
    
    desc += self.__class__(label='Minimum', priority=400, accessor=MAAttrAccessor('min'))
    desc += self.__class__(label='Maximum', priority=410, accessor=MAAttrAccessor('max'))

    return desc
