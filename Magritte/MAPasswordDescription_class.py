from MAStringDescription_class import MAStringDescription

class MAPasswordDescription(MAStringDescription):

    def isSortable(self):
        return False

    def isObfuscated(self, anObject):
        return anObject is not None and isinstance(anObject, str) and len(anObject) > 0 and all(character == "*" for character in anObject)

    def obfuscated(self, anObject):
        return "*" * len(str(anObject))

    def acceptMagritte(self, aVisitor):
        aVisitor.visitPasswordDescription(self)

