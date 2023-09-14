from copy import copy
from sys import intern
from accessors.MANullAccessor_class import MANullAccessor
from MAValidatorVisitor_class import MAValidatorVisitor

from errors.MAValidationError import MAValidationError
from errors.MAConditionError import MAConditionError
from errors.MARequiredError import MARequiredError

class MADescription:

    @classmethod
    def isAbstract(cls):
        return True

    def __init__(self, **kwargs):
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

    def __copy__(self):
        clone = self.__class__()
        clone.__dict__.update(self.__dict__)
        clone.accessor = copy(self.accessor)
        return clone


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
        try:
            return self._kind
        except AttributeError:
            return self.defaultKind()

    @kind.setter
    def kind(self, aClass):
        self._kind = aClass

    @classmethod
    def defaultKind(cls):
        return object

    def isKindDefined(self):
        try:
            return self._kind is not None
        except AttributeError:
            return False


    @property
    def readOnly(self):
        try:
            return self._readOnly
        except AttributeError:
            return self.defaultReadOnly()

    @readOnly.setter
    def readOnly(self, aBool):
        self._readOnly = aBool

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
        try:
            return self._required
        except AttributeError:
            return self.defaultRequired()

    @required.setter
    def required(self, aBool):
        self._required = aBool

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
        try:
            result = self._undefinedValue
        except AttributeError:
            result = self.defaultUndefinedValue()
        return self.defaultUndefinedValue() if result is None else result

    @undefinedValue.setter
    def undefinedValue(self, anObject):
        self._undefinedValue = anObject

    @classmethod
    def defaultUndefinedValue(cls):
        return None


    @property
    def name(self):
        try:
            return self._name
        except AttributeError:
            return self.accessor.name

    @name.setter
    def name(self, aSymbol):
        if aSymbol is None:
            self._name = None
        else:
            self._name = intern(aSymbol)

    @property
    def comment(self):
        try:
            return self._comment
        except AttributeError:
            return self.defaultComment()

    @comment.setter
    def comment(self, aStr):
        self._comment = aStr

    @classmethod
    def defaultComment(cls):
        return None

    def hasComment(self):
        comment = self.comment
        return bool(comment)


    @property
    def group(self):
        try:
            return self._group
        except AttributeError:
            return self.defaultGroup()

    @group.setter
    def group(self, aStr):
        self._group = aStr

    @classmethod
    def defaultGroup(cls):
        return None


    @property
    def label(self):
        try:
            return self._label
        except AttributeError:
            return self.defaultLabel()

    @label.setter
    def label(self, aStr):
        self._label = aStr

    @classmethod
    def defaultLabel(cls):
        return intern('')

    def hasLabel(self):
        label = self.label
        return bool(label)



    @property
    def priority(self):
        try:
            return self._priority
        except AttributeError:
            return self.defaultPriority()

    @priority.setter
    def priority(self, aNumber):
        self._priority = aNumber

    @classmethod
    def defaultPriority(cls):
        return 0


    @property
    def visible(self):
        try:
            return self._visible
        except AttributeError:
            return self.defaultVisible()

    @visible.setter
    def visible(self, aBool):
        self._visible = aBool

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
    def conditions(self):
        try:
            return self._conditions
        except AttributeError:
            self._conditions = self.defaultConditions()
            return self._conditions

    @conditions.setter
    def conditions(self, conditionsTuplesList):
        self._conditions = conditionsTuplesList

    @classmethod
    def defaultConditions(cls):
        return []
        
    def addCondition(self, condition, label=None):
        if(label is None): label = getattr(condition, "label", None)
        self.conditions.append((condition, label)) # double parenthesis is not a typo: we add _tuple_ into `_conditions` list

    @property
    def undefined(self):
        try:
            result = self._undefined
        except AttributeError:
            result = self.defaultUndefined()
        return self.defaultUndefined() if result is None else result
        # The idea behind this double defaultUndefined() call is (I believe) as follows:
        # even if you manually assign None to the `undefined` (i.e. not just left it unmentioned),
        # it still be treated as non-set and return default value.
        # I believe it's to guarantee that `undefined` always returns string...or I don't know 

    @undefined.setter
    def undefined(self, aStr):
        self._undefined_set(aStr) #important to be able to override setter in subclasses

    def _undefined_set(self, aStr):
        self._undefined = aStr

    @classmethod
    def defaultUndefined(cls):
        return intern('')


    def isContainer(self):
        return False

    def isSortable(self):
        return False


    def acceptMagritte(self, aVisitor):
        aVisitor.visitDescription(self)


    # =========== attributes-messages-validation ===========

    @property
    def requiredErrorMessage(self):
        try:
            return self._requiredErrorMessage
        except AttributeError:
            return self.defaultRequiredErrorMessage()

    @requiredErrorMessage.setter
    def requiredErrorMessage(self, message):
        self._requiredErrorMessage = message

    @classmethod
    def defaultRequiredErrorMessage(cls):
        return 'Input is required but no input given'



    @property
    def kindErrorMessage(self):
        try:
            return self._kindErrorMessage
        except AttributeError:
            return self.defaultKindErrorMessage()

    @kindErrorMessage.setter
    def kindErrorMessage(self, message):
        self._kindErrorMessage = message

    @classmethod
    def defaultKindErrorMessage(cls):
        return 'Invalid input given - wrong type'



    @property
    def multipleErrorsMessage(self):
        try:
            return self._multipleErrorsMessage
        except AttributeError:
            return self.defaultMultipleErrorsMessage()

    @multipleErrorsMessage.setter
    def multipleErrorsMessage(self, message):
        self._multipleErrorsMessage = message

    @classmethod
    def defaultMultipleErrorsMessage(cls):
        return 'Multiple errors'



    @property
    def conflictErrorMessage(self):
        try:
            return self._conflictErrorMessage
        except AttributeError:
            return self.defaultConflictErrorMessage()  # Use cls.defaultConflictErrorMessage() instead
    
    @conflictErrorMessage.setter
    def conflictErrorMessage(self, message):
        self._conflictErrorMessage = message
    
    @classmethod
    def defaultConflictErrorMessage(cls):
        return 'Input is conflicting with concurrent modification'

    # =========== /attributes-messages-validation ===========


    # =========== validation ===========

    @classmethod
    def defaultValidator(cls):
        return MAValidatorVisitor

    @property
    def validator(self):
        try:
            return self._validator
        except AttributeError:
            return self.defaultValidator()

    @validator.setter
    def validator(self, aVisitorClass):
        self._validator = aVisitorClass

    def validate(self, model):
        visitor = self.validator()
        errors = visitor.validateUsing(model, self)
        return errors

    def _validateRequired(self, model):
        if self.isRequired() and model is None:
            return [MARequiredError(message = self.requiredErrorMessage, aDescription = self)]
        else:
            return []

    def _validateKind(self, model):
        if not isinstance(model, self.kind):
            return [MARequiredError(message = self.requiredErrorMessage, aDescription = self)]
        else:
            return []

    def _validateSpecific(self, model):
    # validates descriptions-specific conditions. Subclasses may override this method - see MAMAgnitudeDescription for example."
        return []
        
    def _validateConditions(self, model):
        errors = []
        
        for conditionTuple in self.conditions:
            (condition, label) = conditionTuple
            
            try:
                if not condition(model):
                    errors.append(MAConditionError(self, label))
            except MAValidationError as e:
                errors.append(e)
                
        return errors


    # =========== /validation ===========
