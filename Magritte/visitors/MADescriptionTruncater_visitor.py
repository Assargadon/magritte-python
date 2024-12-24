
from copy import copy

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor


class MADescriptionTruncater(MAVisitor):

    def __init__(self):
        super().__init__()
        self._pathes_whitelist = None
        self._keep_element_descriptions = None
        self._truncated_description = None

    def _get_nested_pathes_whitelist(self, current_name: str):
        prefix = f'.{current_name}'
        l = len(prefix)
        nested_pathes_whitelist = []
        for path in self._pathes_whitelist:
            if path == prefix or path.startswith(f'{prefix}.'):
                nested_pathes_whitelist.append(path[l:])
        return nested_pathes_whitelist

    def _next_level(self, name: str, description: MADescription):
        pass

    def truncate(self, description: MADescription, pathes_whitelist: list[str], keep_element_descriptions=True) -> MAContainer:
        self._pathes_whitelist = pathes_whitelist
        self._keep_element_descriptions = keep_element_descriptions
        self._truncated_description = None
        self.visit(description)
        return self._truncated_description


    def visitElementDescription(self, description):
        if self._keep_element_descriptions or len(self._get_nested_pathes_whitelist(description.name)) > 0:
            self._truncated_description = description

    def visitContainer(self, description: MAContainer):
        container = MAContainer()
        for description in description.children:
            self._truncated_description = None
            self.visit(description)
            if self._truncated_description is not None:
                container.children.append(self._truncated_description)
        self._truncated_description = container

    def visitReferenceDescription(self, description: MAReferenceDescription):
        isContainer = isinstance(description.reference, MAContainer)
        if isContainer:
            nested_pathes_whitelist = self._get_nested_pathes_whitelist(description.name)
            if len(nested_pathes_whitelist) > 0:
                # push stack
                pathes_whitelist = self._pathes_whitelist
                self._pathes_whitelist = nested_pathes_whitelist

                # process
                self._truncated_description = None
                self.visit(description.reference)

                if self._truncated_description is not None:
                    description_clone = copy(description)
                    description_clone.reference = self._truncated_description
                    self._truncated_description = description_clone

                # pop stack
                self._pathes_whitelist = pathes_whitelist
        else:
            self.visitElementDescription(description)


if __name__ == '__main__':
    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
    from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer

    descriptors = TestModelDescriptorProvider()
    environment = TestEnvironmentProvider()
    hostDescriptor = descriptors.description_for("Host")
    truncater = MADescriptionTruncater()

    hostDescriptor_truncated = truncater.truncate(
        hostDescriptor,
        [
            '.ports',
        ]
    )
    print(hostDescriptor_truncated)

    host = environment.hosts[0]

    s = MAReferencedDataHumanReadableSerializer()
    d = MAReferencedDataHumanReadableDeserializer()
    host_serialized = s.serializeHumanReadable(host, hostDescriptor)

    print(host_serialized)

    host_deserialized = d.deserializeHumanReadable(host_serialized, hostDescriptor)

    print(host_deserialized)




