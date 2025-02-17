import json
from copy import copy
import logging

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.accessors.MAPluggableAccessor_class import MAPluggableAccessor
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
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
            logger.info(f"{self.__class__.__name__}.walkDescription(): "
                        f"model = {model.__class__.__name__} ({hex(id(model))}) was already visited")
            if len(self.visited_contexts) == 1:
                logger.info(f"{self.__class__.__name__}.walkDescription(): "
                            f"model = {model.__class__.__name__} ({hex(id(model))}) is the root model being visited "
                            f"via a to-one or single-option reference. We are good to go.")
            else:
                ctx = self.visited_contexts[model_id]
                if ctx.processed:
                    # if model was previously visited and processed - return the result
                    logger.info(f"{self.__class__.__name__}.walkDescription(): "
                                f"model = {model.__class__.__name__} ({hex(id(model))}) was already visited "
                                f"and processed")
                    return ctx.result
                else:
                    logger.info(f"{self.__class__.__name__}.walkDescription(): "
                                f"model = {model.__class__.__name__} ({hex(id(model))}): cyclic reference detected")
                    # if model was previously visited and not processed - cyclic reference
                    if not self.skip_cycles:
                        raise CyclicReferenceError(ctx, f"Cyclic reference detected: {ctx}")
                    else:
                        return None

        logger.info(f"{self.__class__.__name__}.walkDescription(): "
                    f"model = {model.__class__.__name__} ({hex(id(model))}) was not visited before. Creating context.")
        context = self.Context(model, description, self.get_model_key())
        self.visited_contexts[model_id] = context
        logger.info(f"{self.__class__.__name__}.walkDescription(): Adding new context to context_stack: {context}")
        self.context_stack.append(context)
        self.current_context = self.context_stack[-1]
        self.visit(description)
        updated_context = self.context_stack.pop()
        updated_context.processed = True
        self.current_context = self.context_stack[-1] if self.context_stack else None
        logger.info(f"{self.__class__.__name__}.walkDescription(): "
                    f"model = {model.__class__.__name__} ({hex(id(model))}). Returning result: {updated_context.result}")
        return updated_context.result

    def _shouldProcessDescription(self, description: MADescription):
        return True

    def visit(self, description: MADescription):
        logger.debug(f"{self.__class__.__name__}.visit() called with "
                     f"description = {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visit(): self.current_context: {self.current_context}")
        if self._shouldProcessDescription(description):
            super().visit(description)
        logger.debug(f"{self.__class__.__name__}.visit returning results for description "
                     f"= {description.name} ({description.__class__.__name__}): {self.current_context}")

    def visitContainer(self, description: MAContainer):
        logger.debug(f"{self.__class__.__name__}.visitContainer() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        self.current_context.elements = []
        self.visitAll(description.children)
        self.current_context.result = self.current_context.elements

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        related_obj = MAModel.readUsingWrapper(self.current_context.model, description)
        if related_obj == description.undefinedValue:
            return None
        if related_obj is not None:
            ref_result = self.walkDescription(related_obj, description.reference)
        else:
            ref_result = None
        self.current_context.elements.append((description, ref_result))
        self.current_context.result = ref_result  # return only the result, in case it is the root model

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        related_objs = MAModel.readUsingWrapper(self.current_context.model, description)
        if related_objs == description.undefinedValue:
            return None
        if related_objs is not None:
            ref_results = []
            for obj in related_objs:
                ref_results.append(self.walkDescription(obj, description.reference))
            self.current_context.elements.append((description, ref_results))
            self.current_context.result = ref_results  # return only the results, in case it is the root model

    def visitSingleOptionDescription(self, description: MASingleOptionDescription):
        logger.debug(f"{self.__class__.__name__}.visitSingleOptionDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        reference = description.reference
        if isinstance(reference, MAContainer):
            self.visitToOneRelationDescription(description)
        elif isinstance(reference, MAElementDescription) and not isinstance(reference, MAReferenceDescription):
            self.visitElementDescription(description)
        else:
            raise TypeError(f"Unsupported reference type in SingleOptionDescription: {type(reference)}")

    def visitElementDescription(self, description: MAElementDescription):
        logger.debug(f"{self.__class__.__name__}.visitElementDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        value = MAModel.readUsingWrapper(self.current_context.model, description)
        if value == description.undefinedValue:
            return None
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
        print(f"{self._c_prefix}Object described by {description.name} ({description.__class__.__name__}): "
              f"{self.current_context.model}")
        super().visitContainer(description)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToOneRelationDescription(description)

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}")
        super().visitToManyRelationDescription(description)

    def visitElementDescription(self, description: MAElementDescription):
        super().visitElementDescription(description)
        print(f"{self._e_prefix}{description.__class__.__name__}: {description.name}: "
              f"{self.current_context.elements[-1][1]}")


class MAReferencedDataHumanReadableSerializer(MADescriptionWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._json_writer = MAValueJsonWriter()

    def walkDescription(self, model, description):
        try:
            return super().walkDescription(model, description)
        except CyclicReferenceError as e:
            return e.ctx.model_key

    def _shouldProcessDescription(self, description: MADescription):
        if not description.isVisible():
            return False
        if (isinstance(description.accessor, MAPluggableAccessor)
                and not description.accessor.canRead(None)):  # MAPluggableAccessor canRead does not depend on model
            return False
        return True

    def visitContainer(self, description: MAContainer):
        super().visitContainer(description)
        obj_dict = {
            "-x-magritte-class": self.current_context.model.__class__.__name__,
            "-x-magritte-key": self.current_context.model_key,
        }
        obj_dict.update({desc.name: value for desc, value in self.current_context.elements})
        self.current_context.result = obj_dict

    def visitElementDescription(self, description: MAElementDescription):
        logger.debug(f"{self.__class__.__name__}.visitElementDescription(): "
                     f"description {description.name} ({description.__class__.__name__})")
        value = MAModel.readUsingWrapper(self.current_context.model, description)
        if value == description.undefinedValue:
            return None
        json_value = self._json_writer.write_json(self.current_context.model, description)
        self.current_context.elements.append((description, json_value))
        self.current_context.result = json_value

    def dumpHumanReadable(self, model, description):
        logger.debug(f"{self.__class__.__name__}.dumpHumanReadable(): "
                     f"description {description.name} ({description.__class__.__name__})")
        self.reset()
        return self.walkDescription(model, description)

    def serializeHumanReadable(self, model, description, indent=None):
        logger.debug(f"{self.__class__.__name__}.serializeHumanReadable(): "
                     f"description {description.name} ({description.__class__.__name__})")
        return json.dumps(self.dumpHumanReadable(model, description), indent=indent)

# Test examples
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(message)s\n')
    # logger.setLevel(logging.DEBUG)

    from Magritte.model_for_tests import Host, User, Organization
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
    
    desc_provider = TestModelDescriptorProvider()
    org = Organization.random_organization()
    user = org.listusers[0]
    host = Host.random_host()
    host.ports = host.ports[:2]
    # host.software = []
    host_desc = desc_provider.description_for("Host")
    
    port_desc = desc_provider.description_for("Port")
    host_ports_desc = copy(host_desc['ports'])
    host_ports_desc.accessor = MAIdentityAccessor()
    port_host_desc = copy(port_desc['host'])
    port_host_desc.accessor = MAIdentityAccessor()
    user_desc = desc_provider.description_for("User")
    user_dob_desc = copy(user_desc['dateofbirth'])
    user_dob_desc.accessor = MAIdentityAccessor()

    class Parent:
        def __init__(self, name):
            self.id = 0
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
            MAIntDescription(name="id", accessor=MAAttrAccessor("id"), visible=False),
            MAStringDescription(name="name", accessor=MAAttrAccessor("name")),
            MAToManyRelationDescription(name="children", accessor=MAAttrAccessor("children"), reference=child_desc)
        ])
    child_desc.setChildren([
            MAStringDescription(name="nick", accessor=MAAttrAccessor("nick"), undefinedValue=""),
            MAToOneRelationDescription(name="parent", accessor=MAAttrAccessor("parent"), reference=parent_desc),
            # MASingleOptionDescription(name="parent", accessor=MAAttrAccessor("parent"), reference=parent_desc)
        ])

    # print(f"child_desc[nick].undefinedValue: {child_desc['nick'].undefinedValue!r}")
    child_parent_desc = copy(child_desc['parent'])
    child_parent_desc.accessor = MAIdentityAccessor()

    parent = Parent("John")
    child = Child("Johnny")
    parent.children = [child]
    child.parent = parent

    child2 = Child("Jenny")
    child3 = Child("")
    child3.parent = parent

    printer = MAReferencedDataPrinter()
    # printer.print(host, host_desc)
    # printer.print(parent, parent_desc)
    # printer.print(host.ports[0], port_desc)
    # printer.print(host.ports, host_ports_desc)
    # printer.print(user, user_desc)

    serializer = MAReferencedDataHumanReadableSerializer()
    # print(serializer.dumpHumanReadable(host, host_desc))
    # print(serializer.serializeHumanReadable(host, host_desc))
    # print(serializer.dumpHumanReadable(host.ports[0], port_desc))
    # print(serializer.serializeHumanReadable(host.ports[0], port_desc))
    # print(serializer.dumpHumanReadable(host.ports, host_ports_desc))
    # print(serializer.serializeHumanReadable(host.ports, host_ports_desc))
    # print(serializer.dumpHumanReadable(host.ports[0].host, port_host_desc))
    # print(serializer.serializeHumanReadable(host.ports[0].host, port_host_desc))
    # print(serializer.dumpHumanReadable(user, user_desc))
    # print(serializer.serializeHumanReadable(user, user_desc))
    # print(serializer.dumpHumanReadable(user.dateofbirth, user_dob_desc))
    # print(serializer.serializeHumanReadable(user.dateofbirth, user_dob_desc))
    # print(serializer.dumpHumanReadable(parent, parent_desc))
    # print(serializer.dumpHumanReadable(child, child_desc))
    # print(serializer.serializeHumanReadable(parent, parent_desc))
    # print(serializer.serializeHumanReadable(child, child_desc))
    # print(serializer.dumpHumanReadable(child2, child_desc))
    # print(serializer.serializeHumanReadable(child2, child_desc))
    # print(serializer.dumpHumanReadable(child3, child_desc))
    # print(serializer.serializeHumanReadable(child3, child_desc, indent=2))
    print(serializer.dumpHumanReadable(child.parent, child_parent_desc))
    print(serializer.serializeHumanReadable(child.parent, child_parent_desc, indent=2))