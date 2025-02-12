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

    def walkDescription(self, model, description):
        """Main method for traversing the description."""
        if model is None or description is None:
            return

        model_id = id(model)
        if model_id in self.visited_objects:
            return  # Skip already visited objects

        self.visited_objects.add(model_id)
        self.model_stack.append(model)
        self.visit(description)
        self.model_stack.pop()

    def visit(self, description: MAElementDescription):
        """Visit the description."""
        self.model = self.model_stack[-1]
        super().visit(description)

    def visitContainer(self, description: MAContainer):
        """Process the container description."""
        self.visitAll(description.children)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        """Process the "one-to-one" relation."""
        related_obj = MAModel.readUsingWrapper(self.model, description)
        self.walkDescription(related_obj, description.reference)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        """Process the "one-to-many" relation."""
        related_objs = MAModel.readUsingWrapper(self.model, description)
        for obj in related_objs:
            self.walkDescription(obj, description.reference)

    def visitElementDescription(self, description: MAElementDescription):
        """Process scalar values."""
        pass

class MAReferencedDataPrinter(MADescriptionWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._indent = '= '
        self._prefix = ''

    def visit(self, description: MAElementDescription):
        self._prefix = self._indent * len(self.model_stack)
        super().visit(description)

    def visitContainer(self, description: MAContainer):
        print(f"{self._prefix}Object described by {description.name} of kind {description.kind}: {self.model}")
        super().visitContainer(description)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        print(f"{self._prefix}One-to-One relation: {description.name} of kind {description.kind}")
        super().visitToOneRelationDescription(description)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        print(f"{self._prefix}One-to-Many relation: {description.name} of kind {description.kind}")
        super().visitToManyRelationDescription(description)

    def visitElementDescription(self, description: MAElementDescription):
        value = MAModel.readUsingWrapper(self.model, description)
        print(f"{self._prefix}- Element: {description.name} of kind {description.kind}: {value}")

# Test examples
if __name__ == "__main__":
    from Magritte.model_for_tests import Host
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider

    desc_provider = TestModelDescriptorProvider()
    host = Host.random_host()
    host_desc = desc_provider.description_for("Host")
    port_desc = desc_provider.description_for("Port")
    printer = MAReferencedDataPrinter()
    # printer.walkDescription(host, host_desc)
    printer.walkDescription(host.ports[0], port_desc)
