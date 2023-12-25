from Magritte.descriptions.MAElementDescription_class import MAElementDescription

class MABooleanDescription(MAElementDescription):
    
    # Except of their own fields, smalltalk original has also #options , #reference and #isExtensible
    # to provide duck-typing compatibility with MAOptionDescription / MASingleOptionDescription
    # as long as it's only used for sharing UI components between boolean and option descriptions,
    # I omit it here - looks like a trick, not natural for the system. But beware in case I'm wrong.  

    def magritteDescription(self):
        from Magritte.descriptions import MABooleanDescription_selfdesc
        return MABooleanDescription_selfdesc.magritteDescription(self, super().magritteDescription())


    @classmethod
    def isAbstract(cls):
        return False

    @classmethod
    def defaultKind(cls):
        return bool

    @property
    def trueString(self):
        try:
            return self._trueString
        except AttributeError:
            return self.defaultTrueString()

    @trueString.setter
    def trueString(self, trueString):
        self._trueString = trueString

    @classmethod
    def defaultTrueString(cls):
         return cls.defaultTrueStrings()[0]

    @classmethod
    def defaultTrueStrings(cls):
         return ['true', 't', 'yes', 'y', '1', 'on']


    @property
    def falseString(self):
        try:
            return self._falseString
        except AttributeError:
            return self.defaultFalseString()

    @falseString.setter
    def falseString(self, falseString):
        self._falseString = falseString

    @classmethod
    def defaultFalseString(cls):
         return cls.defaultFalseStrings()[0]

    @classmethod
    def defaultFalseStrings(cls):
         return ['false', 'f', 'no', 'n', '0', 'off']


    def acceptMagritte(self, aVisitor):
        return aVisitor.visitBooleanDescription(self)
