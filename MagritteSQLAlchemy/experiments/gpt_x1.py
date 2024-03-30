class MyClass:
    def __init__(self, value):
        self.value = value

    def __getattribute__(self, name):
        print(f"Accessing attribute {name}")
        if name == '__dict__':
            return {}
        return super().__getattribute__(name)

obj = MyClass(10)
obj.__dict__['foo'] = 'bar'
obj.__dict__['value'] = 'bar1'

print(obj.__dict__)  # This will trigger the __getattribute__ method
print(obj.value)     # This will also trigger the __getattribute__ method

print(getattr(obj, 'value'))
