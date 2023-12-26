from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.accessors.MADictAccessor_class import MADictAccessor
from Magritte.accessors.MAPluggableAccessor_class import MAPluggableAccessor

from datetime import date

class Person:
    def __init__(self, first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date


model_class_instance = Person("John", "Doe", date(1990, 1, 1))

model_dict = dict(first = "John", last = "Doe", dob = date(1990, 1, 1))

model_array = ["John", "Doe", date(1990, 1, 1)]


desc_class = MAContainer()
desc_class += MAStringDescription(accessor = MAAttrAccessor("first_name"))
desc_class += MAStringDescription(accessor = MAAttrAccessor("last_name"))
desc_class += MADateDescription(accessor = MAAttrAccessor("birth_date"))

desc_dict = MAContainer()
desc_dict += MAStringDescription(accessor = MADictAccessor("first"))
desc_dict += MAStringDescription(accessor = MADictAccessor("last"))
desc_dict += MADateDescription(accessor = MADictAccessor("dob"))

desc_array = MAContainer()
desc_array += MAStringDescription(accessor = MAPluggableAccessor(aReadFunc = lambda model: model[0], aWriteFunc = None))
desc_array += MAStringDescription(accessor = MAPluggableAccessor(aReadFunc = lambda model: model[1], aWriteFunc = None))
desc_array += MADateDescription(accessor = MAPluggableAccessor(aReadFunc = lambda model: model[2], aWriteFunc = None))


def print_by_desc(model, container_description):
    res=""
    for desc in container_description.children:
        res = res + " " + str(desc.accessor.read(model))
    print(res)
    
print_by_desc(model_class_instance, desc_class)
print_by_desc(model_dict, desc_dict)
print_by_desc(model_array, desc_array)
