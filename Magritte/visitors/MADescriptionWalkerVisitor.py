from copy import copy

from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.MAModel_class import MAModel


class MADescriptionWalkerVisitor(MAVisitor):
    def __init__(self):
        super().__init__()
        self.visited_objects = set()
        self.model_stack = []  # Use stack for tracking the current model
        self.model = None

    def reset(self):
        self.visited_objects.clear()
        self.model_stack.clear()
        self.model = None

    def walkDescription(self, model, description):
        """Main method for traversing the description."""
        if description is None:
            raise ValueError("Description cannot be None")
        if model == description.undefinedValue:
            return

        model_id = id(model)
        if model_id in self.visited_objects:
            return  # Skip already visited objects

        self.visited_objects.add(model_id)
        self.model_stack.append(model)
        self.visit(description)
        self.model_stack.pop()

    def visit(self, description: MADescription):
        """Visit the description."""
        self.model = self.model_stack[-1]
        super().visit(description)

    def visitContainer(self, description: MAContainer):
        """Process the container description."""
        self.visitAll(description.children)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        """Process the "one-to-one" relation."""
        related_obj = MAModel.readUsingWrapper(self.model, description)
        if related_obj is not None:
            self.walkDescription(related_obj, description.reference)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        """Process the "one-to-many" relation."""
        related_objs = MAModel.readUsingWrapper(self.model, description)
        if related_objs is not None:
            for obj in related_objs:
                self.walkDescription(obj, description.reference)

    def visitSingleOptionDescription(self, description: MASingleOptionDescription):
        reference = description.reference
        if isinstance(reference, MAContainer):
            self.visitToOneRelationDescription(description)
        elif isinstance(reference, MAElementDescription) and not isinstance(reference, MAToOneRelationDescription):
            self.visitElementDescription(description)
        else:
            raise TypeError(f"Unsupported reference type in SingleOptionDescription: {type(reference)}")

    def visitElementDescription(self, description: MAElementDescription):
        """Process scalar values."""
        pass

class MAReferencedDataPrinter(MADescriptionWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._indent = '= '
        self._level_prefix = ''
        self._elem_prefix = '- '
        self._c_prefix = ''
        self._e_prefix = ''

    def print(self, model, description):
        self.reset()
        print("======================================================")
        self.walkDescription(model, description)
        print("======================================================")

    def visit(self, description: MADescription):
        self._level_prefix = self._indent * len(self.model_stack)
        self._c_prefix = self._level_prefix
        self._e_prefix = self._level_prefix + self._elem_prefix
        super().visit(description)

    def visitContainer(self, description: MAContainer):
        print(f"{self._c_prefix}Object described by {description.name} of kind {description.kind}: {self.model}")
        super().visitContainer(description)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToOneRelationDescription(description)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToManyRelationDescription(description)

    def visitElementDescription(self, description: MAElementDescription):
        value = MAModel.readUsingWrapper(self.model, description)
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name} of kind {description.kind}: {value}")

# Test examples
if __name__ == "__main__":
    from Magritte.model_for_tests import Host, User, Organization
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider

    desc_provider = TestModelDescriptorProvider()
    org = Organization.random_organization()
    host = Host.random_host()
    user = User.random_user(organization=org)
    host_desc = desc_provider.description_for("Host")
    port_desc = desc_provider.description_for("Port")
    host_ports_desc = copy(host_desc['ports'])
    host_ports_desc.accessor = MAIdentityAccessor()
    user_desc = desc_provider.description_for("User")
    printer = MAReferencedDataPrinter()
    printer.print(host, host_desc)
    printer.print(host.ports[0], port_desc)
    printer.print(host.ports, host_ports_desc)
    printer.print(user, user_desc)
