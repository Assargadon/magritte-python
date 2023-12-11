from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

DynamicBase = declarative_base()

# ATTENTION! Please create postgres 'demo_db' database if not exists before run this script

# set the connection string to run this
conn_str = "postgresql://postgres:secret@magritte-python-postgres/demo_db"

def user_table_generator():
    user_table_columns_meta = {'id': {'type': Integer, 'nullable': False, 'primary_key': True},
                               'name': {'type': String(30), 'nullable': True, 'primary_key': False},
                               'fullname': {'type': String, 'nullable': False, 'primary_key': False}}

    user_table_desc = {'__tablename__': 'user_account_dynamic'}

    for key in user_table_columns_meta:
        user_table_desc[key] = Column(user_table_columns_meta[key]['type'],
                                      nullable=user_table_columns_meta[key]['nullable']
                                      , primary_key=user_table_columns_meta[key]['primary_key'])

    return type('UserAccountModel', (DynamicBase,), user_table_desc)


def address_table_generator():
    address_table_columns_meta = {'id': {'type': Integer, 'nullable': False, 'primary_key': True},
                                  'email_address': {'type': String(30), 'nullable': True, 'primary_key': False},
                                  'user_id': {'type': Integer, 'foreign_key': 'user_account_dynamic.id'}}

    address_table_desc = {'__tablename__': 'address_dynamic'}

    for key in address_table_columns_meta:
        if 'foreign_key' in address_table_columns_meta[key]:
            address_table_desc[key] = Column(address_table_columns_meta[key]['type'],
                                             ForeignKey(address_table_columns_meta[key]['foreign_key']))
        else:
            address_table_desc[key] = Column(address_table_columns_meta[key]['type'],
                                             nullable=address_table_columns_meta[key]['nullable']
                                             , primary_key=address_table_columns_meta[key]['primary_key'])

    return type('AddressModel', (DynamicBase,), address_table_desc)


UserAccountModel = user_table_generator()
AddressModel = address_table_generator()

engine = create_engine(conn_str, echo=True)

DynamicBase.metadata.create_all(engine)
