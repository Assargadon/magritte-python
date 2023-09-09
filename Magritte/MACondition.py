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
        return lambda model: model > param

    def __lt__(self, param):
        return lambda model: model < param

    def __ge__(self, param):
        return lambda model: model >= param

    def __le__(self, param):
        return lambda model: model <= param

    def __eq__(self, param):
        return lambda model: model == param

    def __ne__(self, param):
        return lambda model: model != param


class _list_impersonator:
    def isEmpty(self):
        return lambda _list: not _list
        
    def notEmpty(self):
        return lambda _list: not not _list
        
    def contains(self, element): #unfortunately, unlike comparison results, `in` operator converts (coerces) result of __contains__ TO bool
        return lambda _list: element in _list
        

class MACondition:

    model = _model_impersonator()

    list = _list_impersonator()
