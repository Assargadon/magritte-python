import json
from copy import copy
import logging

from typing_extensions import override

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.visitors.MAJson_visitors import MAValueJsonWriter
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAElementDescription_class import MAElementDescription
from Magritte.descriptions.MAToOneRelationDescription_class import MAToOneRelationDescription
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.MAModel_class import MAModel

logger = logging.getLogger(__name__)


class CyclicReferenceError(Exception):
    def __init__(self, ctx, message):
        self.ctx = ctx
        super().__init__(message)


class MADescriptionWalkerVisitor(MAVisitor):

    class Context:
        def __init__(self, model, description, model_key, elements=None, processed=False, result=None):
            self.model = model
            self.description = description
            self.model_key = model_key
            self.elements = elements or []
            self.processed = processed
            self.result = result

        def __repr__(self):
            return (f"Context(model={self.model}, description={self.description}, model_key={self.model_key}, "
                   f"elements={self.elements}, processed={self.processed}, result={self.result})")

    def __init__(self, skip_cycles=False):
        super().__init__()
        self.visited_contexts = {}
        self.context_stack = []
        self._model_key = 0
        self.current_context = None
        self.skip_cycles = skip_cycles

    def reset(self):
        self.visited_contexts.clear()
        self.context_stack.clear()
        self._model_key = 0
        self.current_context = None

    def get_model_key(self):
        res = self._model_key
        self._model_key += 1
        return res

    def walkDescription(self, model, description):
        logger.info(f"{self.__class__.__name__}.walkDescription() called: "
                    f"model = {model.__class__.__name__} ({hex(id(model))}), "
                    f"description = {description.name} ({description.__class__.__name__})")
        if description is None:
            raise ValueError("Description cannot be None")
        if model == description.undefinedValue:
            return None

        model_id = id(model)
        if model_id in self.visited_contexts:
            logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}) was already visited")
            ctx = self.visited_contexts[model_id]
            if ctx.processed:
                # if model was previously visited and processed - return the result
                logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}) was already visited and processed")
                return ctx.result
            else:
                logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}): cyclic reference detected")
                # if model was previously visited and not processed - cyclic reference
                if not self.skip_cycles:
                    raise CyclicReferenceError(ctx, f"Cyclic reference detected: {ctx}")
                else:
                    return None

        context = self.Context(model, description, self.get_model_key())
        self.visited_contexts[model_id] = context
        logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}) was not visited before. Adding to context_stack: {context}")
        self.context_stack.append(context)
        self.current_context = self.context_stack[-1]
        self.visit(description)
        logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}) has just been visited. self.current_context: {self.current_context}")
        updated_context = self.context_stack.pop()
        self.current_context = self.context_stack[-1] if self.context_stack else None
        logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}) has been visited. Updated context: {updated_context}")
        updated_context.processed = True
        logger.info(f"{self.__class__.__name__}.walkDescription(): model = {model.__class__.__name__} ({hex(id(model))}). Returning result: {updated_context.result}")
        return updated_context.result

    def visit(self, description: MADescription):
        logger.debug(f"{self.__class__.__name__}.visit() called with description = {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visit(): self.current_context: {self.current_context}")
        super().visit(description)
        logger.debug(f"{self.__class__.__name__}.visit returning results for description = {description.name} ({description.__class__.__name__}): {self.current_context}")

    def visitContainer(self, description: MAContainer):
        logger.debug(f"{self.__class__.__name__}.visitContainer() called for description {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visitContainer(): self.current_context: {self.current_context}")
        self.current_context.elements = []
        self.visitAll(description.children)
        self.current_context.result = self.current_context.elements
        logger.debug(f"{self.__class__.__name__}.visitContainer returning result: {self.current_context.result}")

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription() called for description {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription(): self.current_context: {self.current_context}")
        related_obj = MAModel.readUsingWrapper(self.current_context.model, description)
        if related_obj is not None:
            ref_result = self.walkDescription(related_obj, description.reference)
        else:
            ref_result = None
        self.current_context.elements.append((description, ref_result))
        self.current_context.result = ref_result  # return only the result, in case it is the root model
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription returning result: {ref_result}")

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription() called for description {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription(): self.current_context: {self.current_context}")
        related_objs = MAModel.readUsingWrapper(self.current_context.model, description)
        if related_objs is not None:
            ref_results = []
            for obj in related_objs:
                ref_results.append(self.walkDescription(obj, description.reference))
            self.current_context.elements.append((description, ref_results))
            self.current_context.result = ref_results  # return only the results, in case it is the root model
            logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription returning result: {ref_results}")

    def visitSingleOptionDescription(self, description: MASingleOptionDescription):
        logger.debug(f"{self.__class__.__name__}.visitSingleOptionDescription() called for description {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visitSingleOptionDescription(): self.current_context: {self.current_context}")
        reference = description.reference
        if isinstance(reference, MAContainer):
            self.visitToOneRelationDescription(description)
        elif isinstance(reference, MAElementDescription) and not isinstance(reference, MAToOneRelationDescription):
            self.visitElementDescription(description)
        else:
            raise TypeError(f"Unsupported reference type in SingleOptionDescription: {type(reference)}")

    def visitElementDescription(self, description: MAElementDescription):
        logger.debug(f"{self.__class__.__name__}.visitElementDescription() called for description {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visitElementDescription(): self.current_context: {self.current_context}")
        value = MAModel.readUsingWrapper(self.current_context.model, description)
        self.current_context.elements.append((description, value))
        self.current_context.result = value  # return only the result, in case it is the root model


class MAReferencedDataPrinter(MADescriptionWalkerVisitor):
    def __init__(self):
        super().__init__(skip_cycles=True)
        # super().__init__()
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
        self._level_prefix = self._indent * len(self.context_stack)
        self._c_prefix = self._level_prefix
        self._e_prefix = self._level_prefix + self._elem_prefix
        super().visit(description)

    def visitContainer(self, description: MAContainer):
        print(f"{self._c_prefix}Object described by {description.name} ({description.__class__.__name__}): {self.current_context.model}")
        super().visitContainer(description)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToOneRelationDescription(description)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToManyRelationDescription(description)

    def visitElementDescription(self, description: MAElementDescription):
        super().visitElementDescription(description)
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}: {self.current_context.elements[-1][1]}")


class MAReferencedDataHumanReadableSerializer(MADescriptionWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._json_writer = MAValueJsonWriter()

    def walkDescription(self, model, description):
        try:
            return super().walkDescription(model, description)
        except CyclicReferenceError as e:
            return e.ctx.model_key

    def visitContainer(self, description: MAContainer):
        logger.debug(f"{self.__class__.__name__}.visitContainer {description.name} of kind {description.kind}")
        super().visitContainer(description)
        obj_dict = {
            "-x-magritte-class": self.current_context.model.__class__.__name__,
            "-x-magritte-key": self.current_context.model_key,
        }
        obj_dict.update({desc.name: value for desc, value in self.current_context.elements})
        self.current_context.result = obj_dict

    def visitElementDescription(self, description: MAElementDescription):
        logger.debug(f"{self.__class__.__name__}.visitElementDescription(): description {description.name} ({description.__class__.__name__})")
        value = MAModel.readUsingWrapper(self.current_context.model, description)
        self.current_context.elements.append((description, value))
        # self.current_context.elements.append((description, self._json_writer.write_json(self.current_context.model, description)))

    def dumpHumanReadable(self, model, description):
        logger.debug(f"{self.__class__.__name__}.dumpHumanReadable(): description {description.name} ({description.__class__.__name__})")
        self.reset()
        return self.walkDescription(model, description)

    def serializeHumanReadable(self, model, description):
        logger.debug(f"{self.__class__.__name__}.serializeHumanReadable(): description {description.name} ({description.__class__.__name__})")
        return json.dumps(self.dumpHumanReadable(model, description), indent=2)

# Test examples
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(message)s\n')
    # logger.setLevel(logging.DEBUG)

    from Magritte.model_for_tests import Host, User, Organization
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
    
    desc_provider = TestModelDescriptorProvider()
    # org = Organization.random_organization()
    # user = User.random_user(organization=org)
    host = Host.random_host()
    host.ports = host.ports[:2]
    host.software = []
    host_desc = desc_provider.description_for("Host")
    
    port_desc = desc_provider.description_for("Port")
    host_ports_desc = copy(host_desc['ports'])
    host_ports_desc.accessor = MAIdentityAccessor()
    user_desc = desc_provider.description_for("User")

    class Parent:
        def __init__(self, name):
            self.name = name
            self.children = []

        def __repr__(self):
            return f"Parent({self.name})"

    class Child:
        def __init__(self, nick):
            self.nick = nick
            self.parent = None

        def __repr__(self):
            return f"Child({self.nick})"

    parent_desc = MAContainer(name="Parent", kind=Parent)
    child_desc = MAContainer(name="Child", kind=Child)
    parent_desc.setChildren([
            MAStringDescription(name="name", accessor=MAAttrAccessor("name")),
            MAToManyRelationDescription(name="children", accessor=MAAttrAccessor("children"), reference=child_desc)
        ])
    child_desc.setChildren([
            MAStringDescription(name="nick", accessor=MAAttrAccessor("nick")),
            MAToOneRelationDescription(name="parent", accessor=MAAttrAccessor("parent"), reference=parent_desc)
        ])

    parent = Parent("John")
    child = Child("Johnny")
    parent.children = [child]
    child.parent = parent

    printer = MAReferencedDataPrinter()
    # printer.print(host, host_desc)
    # printer.print(parent, parent_desc)
    # printer.print(host.ports[0], port_desc)
    # printer.print(host.ports, host_ports_desc)
    # printer.print(user, user_desc)

    serializer = MAReferencedDataHumanReadableSerializer()
    # print(serializer.dumpHumanReadable(parent, parent_desc))
    # print(serializer.dumpHumanReadable(child, child_desc))
    # print(serializer.serializeHumanReadable(parent, parent_desc))
    # print(serializer.serializeHumanReadable(child, child_desc))
    # print(serializer.dumpHumanReadable(host, host_desc))
    print(serializer.serializeHumanReadable(host, host_desc))
    # print(serializer.dumpHumanReadable(host.ports[0], port_desc))
    # print(serializer.serializeHumanReadable(host.ports[0], port_desc))
    # print(serializer.dumpHumanReadable(host.ports, host_ports_desc))
    # print(serializer.serializeHumanReadable(host.ports, host_ports_desc))