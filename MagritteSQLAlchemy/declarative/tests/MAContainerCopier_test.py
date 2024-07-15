from datetime import date
from pprint import pprint

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
from MagritteSQLAlchemy.declarative.MAContainerCopier import MAContainerCopier

from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider


class PersonSrc:
    def __init__(self, first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date


src_instance = PersonSrc("John", "Doe", date(1990, 1, 1))

src_desc_ex = MAContainer()
src_desc_ex += MAStringDescription(accessor=MAAttrAccessor('first_name'))
src_desc_ex += MAStringDescription(accessor=MAAttrAccessor('last_name'))
src_desc_ex += MADateDescription(accessor=MAAttrAccessor('birth_date'))


class PersonDest:
    def __init__(self, first_name, last_name, birth_date):
        self.first_name_dest = first_name
        self.last_name_dest = last_name
        self.birth_date_dest = birth_date


dest_desc_ex = MAContainer()
dest_desc_ex += MAStringDescription(name='first_name', accessor=MAAttrAccessor('first_name_dest'))
dest_desc_ex += MAStringDescription(name='last_name', accessor=MAAttrAccessor('last_name_dest'))
dest_desc_ex += MADateDescription(name='birth_date', accessor=MAAttrAccessor('birth_date_dest'))

dest_instance = PersonDest('', '', '')

maContainerCopier = MAContainerCopier()

maContainerCopier.copy(src_instance, src_desc_ex, dest_instance, dest_desc_ex)
pprint(vars(src_instance))
pprint(vars(dest_instance))

env_src = TestEnvironmentProvider()
env_dest = TestEnvironmentProvider()
descriptors = TestModelDescriptorProvider()


def copy_organization():
    org_desc = descriptors.description_for("Organization")

    pprint("Src organization:")
    pprint(vars(env_src.organization))
    pprint("Dest organization before copy:")
    pprint(vars(env_dest.organization))

    maContainerCopier.copy(env_src.organization, org_desc, env_dest.organization, org_desc)

    pprint("Dest organization after copy::")
    pprint(vars(env_dest.organization))


def copy_list(src_list, dest_list, list_desc, model_name):
    pprint(f"Src {model_name}:")
    for item in src_list:
        pprint(vars(item))

    pprint(f"Dest {model_name} before copy:")
    for item in dest_list:
        pprint(vars(item))

    for idx, item in enumerate(src_list):
        maContainerCopier.copy(item, list_desc, dest_list[idx], list_desc)

    pprint(f"Dest {model_name} after copy::")
    for item in dest_list:
        pprint(vars(item))


copy_organization()
copy_list(env_src.users, env_dest.users, descriptors.description_for("User"), 'user')
copy_list(env_src.accounts, env_dest.accounts, descriptors.description_for("Account"), 'account')
copy_list(env_src.ports, env_dest.ports, descriptors.description_for("Port"), 'port')
copy_list(env_src.hosts, env_dest.hosts, descriptors.description_for("Host"), 'host')


###
# conn_str = "postgresql://postgres:secret@magritte-python-postgres/sqlalchemy_test"
# engine = create_engine(conn_str, echo=True)
# session = Session(engine)

# modelGen = SQLAlchemyModelGenerator()
# acc_model = modelGen.generate_model(TestModelDescriptor.description_for("Account"))
# user_model = modelGen.generate_model(TestModelDescriptor.description_for("User"))

# port_desc = TestModelDescriptor.description_for("Port")
# port_model = modelGen.generate_model(port_desc)

#port_sql_instance = host_model(ip='234', port='01')
#maContainerCopier.copy(env_src.organization, host_desc, host_sql_instance, host_desc)

# host_desc = TestModelDescriptor.description_for("Host")
# host_model = modelGen.generate_model(host_desc)
# modelGen.base_class.metadata.create_all(engine)

# host_select = session.scalar(select(host_model))
# res = session.execute(host_select)

#print(host_sql_instance)

# maContainerCopier.copy(env_src.organization, host_desc, host_sql_instance, host_desc)

# session.add(host_sql_instance)

# user_model = modelGen.generate_model(TestModelDescriptor.description_for("User"))
# acc_model = modelGen.generate_model(TestModelDescriptor.description_for("Account"))
# host_model = modelGen.generate_model(TestModelDescriptor.description_for("Port"))
# port_model = modelGen.generate_model(TestModelDescriptor.description_for("Host"))