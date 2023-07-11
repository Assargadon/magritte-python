
from sys import intern
from MANullAccessor_class import MANullAccessor

class MADescription:

    @classmethod
    def isAbstract(cls):
        return True

    def __init__(self):
        self._propertyDict = {}
        self._accessor = None

    def __eq__(self, other):
        return self._propertyDict == other._propertyDict and self.accessor == other.accessor

    def __setitem__(self, prop_name, value):
        self._propertyDict[prop_name] = value

    def __contains__(self, prop_name):
        return prop_name in self._propertyDict

    def _getOrDefaultIfAbsent(self, prop_name, default_getter):
        if prop_name in self._propertyDict:
            return self._propertyDict[prop_name]
        return default_getter()

    def _getOrDefaultIfAbsentOrNone(self, prop_name, default_getter):
        if prop_name in self._propertyDict:
            value = self._propertyDict[prop_name]
            if value is not None: return value
        return default_getter()


    @property
    def accessor(self):
        if self._accessor is None:
            self._accessor = self.defaultAccessor()
        return self._accessor

    @accessor.setter
    def accessor(self, anObject):
        self._accessor = anObject

    @classmethod
    def defaultAccessor(cls):
        return MANullAccessor()


    @property
    def kind(self):
        return self._getOrDefaultIfAbsent(intern('kind'), self.defaultKind)

    @kind.setter
    def kind(self, aClass):
        self[intern('kind')] = aClass

    @classmethod
    def defaultKind(cls):
        return object

    def isKindDefined(self):
        return intern('kind') in self

    @property
    def kindErrorMessage(self):
        return self._getOrDefaultIfAbsent(intern('kindErrorMessage'), lambda: 'Invalid input given')

    @kindErrorMessage.setter
    def kindErrorMessage(self, aStr):
        self[intern('kindErrorMessage')] = aStr


    @property
    def readOnly(self):
        return self._getOrDefaultIfAbsent(intern('readOnly'), self.defaultReadOnly)

    @readOnly.setter
    def readOnly(self, aBool):
        self[intern('readOnly')] = aBool

    @classmethod
    def defaultReadOnly(cls):
        return False

    def isReadOnly(self):
        return self.readOnly

    def beReadOnly(self):
        self.readOnly = True

    def beWriteable(self):
        self.readOnly = False


    @property
    def required(self):
        return self._getOrDefaultIfAbsent(intern('required'), self.defaultRequired)

    @required.setter
    def required(self, aBool):
        self[intern('required')] = aBool

    @classmethod
    def defaultRequired(cls):
        return False

    def isRequired(self):
        return self.required

    def beRequired(self):
        self.required = True

    def beOptional(self):
        self.required = False


    @property
    def default(self):
        return self.undefinedValue

    @default.setter
    def default(self, anObject):
        pass

    @classmethod
    def defaultDefault(cls):
        return None

    @property
    def undefinedValue(self):
        return self._getOrDefaultIfAbsentOrNone(intern('undefinedValue'), self.defaultUndefinedValue)

    @undefinedValue.setter
    def undefinedValue(self, anObject):
        self[intern('undefinedValue')] = anObject

    @classmethod
    def defaultUndefinedValue(cls):
        return None


    @property
    def name(self):
        return self._getOrDefaultIfAbsent(intern('name'), lambda: self.accessor.name)

    @name.setter
    def name(self, aStr):
        self[intern('name')] = aStr


    @property
    def comment(self):
        return self._getOrDefaultIfAbsent(intern('comment'), self.defaultComment)

    @comment.setter
    def comment(self, aStr):
        self[intern('comment')] = aStr

    @classmethod
    def defaultComment(cls):
        return None

    def hasComment(self):
        comment = self.comment
        return bool(comment)


    @property
    def group(self):
        return self._getOrDefaultIfAbsent(intern('group'), self.defaultGroup)

    @group.setter
    def group(self, aStr):
        self[intern('group')] = aStr

    @classmethod
    def defaultGroup(cls):
        return None


    @property
    def label(self):
        return self._getOrDefaultIfAbsent(intern('label'), self.defaultLabel)

    @label.setter
    def label(self, aStr):
        self[intern('label')] = aStr

    @classmethod
    def defaultLabel(cls):
        return intern('')

    def hasLabel(self):
        label = self.label
        return bool(label)



    @property
    def priority(self):
        return self._getOrDefaultIfAbsent(intern('priority'), self.defaultPriority)

    @priority.setter
    def priority(self, aNumber):
        self[intern('priority')] = aNumber

    @classmethod
    def defaultPriority(cls):
        return 0


    @property
    def visible(self):
        return self._getOrDefaultIfAbsent(intern('visible'), self.defaultVisible)

    @visible.setter
    def visible(self, aBool):
        self[intern('visible')] = aBool

    @classmethod
    def defaultVisible(cls):
        return True

    def isVisible(self):
        return self.readOnly

    def beVisible(self):
        self.readOnly = True

    def beHidden(self):
        self.visible = False



    @property
    def undefined(self):
        return self._getOrDefaultIfAbsentOrNone(intern('undefined'), self.defaultUndefined)

    @undefined.setter
    def undefined(self, aStr):
        self[intern('undefined')] = aStr

    @classmethod
    def defaultUndefined(cls):
        return intern('')


    def isSortable(self):
        return False

    def acceptMagritte(self, aVisitor):
        aVisitor.visitDescription(self)
