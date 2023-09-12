import types

'''
Magritte conditions are just Callables returning True or False and accepting model as parameter
MACondition is just a syntax sugar for commonly used cases:
you may do something like 
```
  condition = MACondition.model > 5
  if(condition(myCounter)):
    //...something...
```
'''

class _model_impersonator:
    def __gt__(self, param):
        return MACondition(lambda model: model > param, f"should be greater than {param}")

    def __lt__(self, param):
        return MACondition(lambda model: model < param, f"should be lower than {param}")

    def __ge__(self, param):
        return MACondition(lambda model: model >= param, f"should be greater than or equal to {param}")

    def __le__(self, param):
        return MACondition(lambda model: model <= param, f"should be less than or equal to {param}")

    def __eq__(self, param):
        return MACondition(lambda model: model == param, f"should be equal to {param}")

    def __ne__(self, param):
        return MACondition(lambda model: model != param, f"should'nt be equal to {param}")


class _list_impersonator:
    def isEmpty(self):
        return MACondition(lambda _list: not _list, f"is empty")
        
    def notEmpty(self):
        return MACondition(lambda _list: not not _list, f"is not empty")
        
    def contains(self, element): #unfortunately, unlike comparison results, `in` operator converts (coerces) result of __contains__ TO bool
        return MACondition(lambda _list: element in _list, f"'{element}' is not in the list")


class MACondition:

    model = _model_impersonator()

    list = _list_impersonator()

    def __init__(self, _callable, label = None):
        self._callable = _callable
        self.label = label
    
    def __call__(self, args):
        return self._callable(args)
    
    def __bool__(self): # this one needed to block "true logical" operators `and`, `or` and `not`
        raise Exception("MACondition does not supports logical expressions. Use lambda-function instead.")

    def __and__(self, operand): # this is to block `&` operator (technically it is bitwise operator, not logical)
        raise Exception("MACondition does not supports logical expressions. Use lambda-function instead.")

    def __or__(self, operand): # block for `|`
        raise Exception("MACondition does not supports logical expressions. Use lambda-function instead.")

    def __not__(self): # block for `~` (bitwize not)
        raise Exception("MACondition does not supports logical expressions. Use lambda-function instead.")

    # One day we may be implement some support for logical operators.
    # (not _really_ logical, because `and`, `or` and `not` cannot be overwritten, and they have no magic functions.
    # But `&`, `|` and `~` _have_ magic functions...well, they expecte dto be bitwize operators, but we can use them for our needs)
