
import types
from copy import copy
from sys import intern
from MANullAccessor_class import MANullAccessor

class MADescription:

    @classmethod
    def isAbstract(cls):
        return True

    def __init__(self, **kwargs):
        self._propertyDict = {}
        self._accessor = self.defaultAccessor()
        for key, value in kwargs.items():
            attr = getattr(self.__class__, key)
            if isinstance(attr, property):
                setattr(self, key, value)
                #attr.fset(self, value)
            #elif isinstance(attr, types.FunctionType):
            #    if attr.__code__.co_argcount == 1:
            #        attr(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.accessor == other.accessor

    def __hash__(self):
        h1 = hash(type(self))
        h2 = hash(self.accessor)
        return h1 ^ h2

    def __lt__(self, other):
        return self.priority < other.priority

    def __getitem__(self, prop_name):
        return self._propertyDict[prop_name]

    def __setitem__(self, prop_name, value):
        self._propertyDict[prop_name] = value

    def __contains__(self, prop_name):
        return prop_name in self._propertyDict

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.accessor = copy(self.accessor)
        return clone

    def get(self, prop_name, default_value):
        return self._propertyDict.get(prop_name, default_value)



    @property
    def accessor(self):
        return self._accessor

    @accessor.setter
    def accessor(self, anObject):
        self._accessor = anObject

    @classmethod
    def defaultAccessor(cls):
        return MANullAccessor()


    @property
    def kind(self):
        return self.get(intern('kind'), self.defaultKind())

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
        return self.get(intern('kindErrorMessage'), 'Invalid input given')

    @kindErrorMessage.setter
    def kindErrorMessage(self, aStr):
        self[intern('kindErrorMessage')] = aStr


    @property
    def readOnly(self):
        return self.get(intern('readOnly'), self.defaultReadOnly())

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
        return self.get(intern('required'), self.defaultRequired())

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
        result = self.get(intern('undefinedValue'), self.defaultUndefinedValue())
        return self.defaultUndefinedValue() if result is None else result

    @undefinedValue.setter
    def undefinedValue(self, anObject):
        self[intern('undefinedValue')] = anObject

    @classmethod
    def defaultUndefinedValue(cls):
        return None


    @property
    def name(self):
        return self.get(intern('name'), self.accessor.name)

    @name.setter
    def name(self, aSymbol):
        if aSymbol is None:
            self[intern('name')] = None
        else:
            self[intern('name')] = intern(aSymbol)

    @property
    def comment(self):
        return self.get(intern('comment'), self.defaultComment())

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
        return self.get(intern('group'), self.defaultGroup())

    @group.setter
    def group(self, aStr):
        self[intern('group')] = aStr

    @classmethod
    def defaultGroup(cls):
        return None


    @property
    def label(self):
        return self.get(intern('label'), self.defaultLabel())

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
        return self.get(intern('priority'), self.defaultPriority())

    @priority.setter
    def priority(self, aNumber):
        self[intern('priority')] = aNumber

    @classmethod
    def defaultPriority(cls):
        return 0


    @property
    def visible(self):
        return self.get(intern('visible'), self.defaultVisible())

    @visible.setter
    def visible(self, aBool):
        self[intern('visible')] = aBool

    @classmethod
    def defaultVisible(cls):
        return True

    def isVisible(self):
        return self.visible

    def beVisible(self):
        self.visible = True

    def beHidden(self):
        self.visible = False



    @property
    def undefined(self):
        result = self.get(intern('undefined'), self.defaultUndefined())
        return self.defaultUndefined() if result is None else result
        # The idea behind this double defaultUndefined() call is (I believe) as follows:
        # even if you manually assign None to the `undefined` (i.e. not just left it unmentioned),
        # it still be treated as non-set and return default value.
        # I believe it's to guarantee that `undefined` always returns string...or I don't know 

    @undefined.setter
    def undefined(self, aStr):
        self[intern('undefined')] = aStr

    def _undefined(self, aStr):
        self[intern('undefined')] = aStr

    @classmethod
    def defaultUndefined(cls):
        return intern('')


    def isContainer(self):
        return False

    def isSortable(self):
        return False


    def acceptMagritte(self, aVisitor):
        aVisitor.visitDescription(self)
