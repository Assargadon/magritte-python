from Magritte.descriptions.MAElementDescription_class import MAElementDescription
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
        src_data = src_accessor.read(self._src)
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


class MAContainerCopierError(MAError):
    pass
