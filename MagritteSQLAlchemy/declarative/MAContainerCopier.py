from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MARelationDescription_class import MARelationDescription
from Magritte.errors.MAError import MAError
from Magritte.visitors.MAVisitor_class import MAVisitor


class MAContainerCopier(MAVisitor):
    _src = None
    _dest = None
    _dest_desc = None

    def copy(self, src, src_desc, dest, dest_desc):
        self._src = src
        self._dest = dest
        self._dest_desc = dest_desc
        self.visitAll(src_desc.children)

    def visitElementDescription(self, element_description: MAElementDescription):
        try:
            src_accessor = getattr(element_description, 'accessor')
        except AttributeError:
            raise MAContainerCopierError('Source descriptor element has no accessor')

        try:
            src_data = src_accessor.read(self._src)
        except:
            return

        dest_element = next((dest_element for dest_element in self._dest_desc.children
                             if dest_element.name == element_description.name), None)
        if dest_element is None:
            raise MAContainerCopierError(f'The destination descriptor has no children of the name attribute have the '
                                         f'"{element_description.name}" value ')
        try:
            dest_accessor = getattr(dest_element, 'accessor')
        except AttributeError:
            raise MAContainerCopierError('Destination descriptor element has no accessor')
        dest_accessor.write(self._dest, src_data)


class MAContainerDbCopier(MAContainerCopier):
    def visitToManyRelationDescription(self, element_description: MARelationDescription):
        to_many_src_data_list = getattr(self._src, element_description.sa_fieldName)
        dest_data_list = getattr(self._dest, element_description.sa_fieldName)
        for data in to_many_src_data_list:
            to_many_dest_instance = getattr(type(self._dest), element_description.sa_fieldName)
            to_many_dest_model_instance = to_many_dest_instance.comparator.entity.class_()
            to_many_dest_model_instance.copy_from(data)
            dest_data_list.append(to_many_dest_model_instance)

    def visitToOneRelationDescription(self, element_description: MARelationDescription):
        pass


class MAContainerCopierError(MAError):
    pass
