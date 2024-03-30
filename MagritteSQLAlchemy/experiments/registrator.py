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
  

def attach_getattribute(cls):
    old_getattribute = cls.__getattribute__
    # for __dict__ return antiwrapper, for other attributes call old_getattribute
    def new_getattribute(self, attr):
        print(f"getattribute {attr}")
        if attr == '__dict__':
            return {'numofport': 42, 'id': random.randint(1, 100000)}
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

        attach_getattribute(descriptor.kind)
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
