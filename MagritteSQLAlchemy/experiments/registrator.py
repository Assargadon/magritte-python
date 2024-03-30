from sqlalchemy import Table, Column, Integer

from Magritte.descriptions.MAContainer_class import MAContainer
from sqlalchemy.orm import registry as sa_registry

from MagritteSQLAlchemy.experiments.fieldsmapper import FieldsMapper

import random

from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription


class CustomDict(dict):
    def __init__(self, original_dict):
        self.original_dict = original_dict
        print(f"CustomDict initialized with type {type(original_dict)} and structure {dir(original_dict)}")

    def __getattr__(self, name): #track unimplemented methods
        print(f"requested unknown attribute (method?) = {name}")

    def __getitem__(self, key):
        print (f"requested key = {key}")
        if key == 'numofport':
            return 42
        elif key == 'id':
            return random.randint(1, 100000)
        else:
            return self.original_dict.__getitem__(key)
  

class DictWrapper:
    def __init__(self , original_dict, model, description):
        self._dict = original_dict
        self.model = model
        self.description = description

    def __getitem__(self, key):
        print(f"Getting item: {key}")
        if key == 'numofport':
            return 42
        return self._dict[key]

    def __setitem__(self, key, value):
        print(f"Setting item: {key} = {value}")
        self._dict[key] = value

    def __delitem__(self, key):
        print(f"Deleting item: {key}")
        del self._dict[key]

    def __contains__(self, key):
        print(f"Checking if {key} is in dict")
        return key in self._dict

    def __len__(self):
        print("Getting length of dict")
        return len(self._dict)

    def __iter__(self):
        print("Iterating over dict")
        return iter(self._dict)

    def __str__(self):
        print("Converting dict to string")
        return str(self._dict)

    def __repr__(self):
        print("Representing dict")
        return repr(self._dict)

    def clear(self):
        print("Clearing dict")
        self._dict.clear()

    def copy(self):
        print("Copying dict")
        return self._dict.copy()

    def get(self, key, default=None):
        print(f"Getting item with default: {key}, {default}")
        return self._dict.get(key, default)

    def items(self):
        print("Getting items of dict")
        return self._dict.items()

    def keys(self):
        print("Getting keys of dict")
        return self._dict.keys()

    def pop(self, key, default=None):
        print(f"Popping item: {key}, {default}")
        return self._dict.pop(key, default)

    def popitem(self):
        print("Popping item")
        return self._dict.popitem()

    def setdefault(self, key, default=None):
        print(f"Setting default for key: {key}, {default}")
        return self._dict.setdefault(key, default)

    def update(self, *args, **kwargs):
        print(f"Updating dict with: {args}, {kwargs}")
        self._dict.update(*args, **kwargs)

    def values(self):
        print("Getting values of dict")
        return self._dict.values()


def attach_getattribute(cls, desc):
    old_getattribute = cls.__getattribute__
    # for __dict__ return antiwrapper, for other attributes call old_getattribute
    def new_getattribute(self, attr):
        #print(f"getattribute {attr}")
        if attr == '__dict__':
            mydict = DictWrapper({'numofport': random.randint(22, 250), 'id': random.randint(1, 100000)}, self, desc)
            return mydict
#            if(hasattr(self, 'antiwrapper')):
#                return self.antiwrapper
#            else:
#                self.antiwrapper = CustomDict(old_getattribute(self, '__dict__'))
#                return self.antiwrapper    
        else:
            return old_getattribute(self, attr)
    cls.__getattribute__ = new_getattribute
    print(f"attached antiwrapper for {cls} for __dict__")

def register(*descriptors: MAContainer, registry: sa_registry = None) -> sa_registry:

    if not registry:
        registry = sa_registry()
    fields_mapper = FieldsMapper()

    for descriptor in descriptors:
        print(descriptor.name)

        table = Table(
            descriptor.name,
            registry.metadata,
            )

        table.append_column(Column("id", Integer, primary_key=True))

        fields_mapper.map(descriptor, table)

        print(f'TABLE: {table.c}')

        properties_to_map = {}
        for desc in descriptor.children:
            print(f'desc = {desc}, desc.name = {desc.name}, is reference = {isinstance(desc, MAReferenceDescription)}')
            if not isinstance(desc, MAReferenceDescription):
                properties_to_map[desc.name] = table.c[desc.name]

        registry.map_imperatively(
            descriptor.kind,
            table,
            properties=properties_to_map,
            )
        print(f'KIND: {dir(descriptor.kind)}')

        attach_getattribute(descriptor.kind, descriptor)
        '''
        properties={
            "addresses": relationship(
                Address,
                back_populates="user",
                ),
            "nick": user_table.c.nickname,
            },
        '''

        '''
        registry.map_imperatively(descriptor.cls, descriptor.table)
        for rel in descriptor.relations:
            registry.map_imperatively(rel.cls, rel.table, properties=rel.properties)
        '''

    return registry
