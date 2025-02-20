import json
from copy import copy
import logging
from typing import Any

from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor
from Magritte.accessors.MAPluggableAccessor_class import MAPluggableAccessor
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MASingleOptionDescription_class import MASingleOptionDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.errors.MAKindError import MAKindError
from Magritte.visitors.MAJson_visitors import MAValueJsonWriter, MAValueJsonReader
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


class DuplicateViewError(Exception):
    def __init__(self, ctx, message):
        self.ctx = ctx
        super().__init__(message)


class MADescriptionWalkerVisitor(MAVisitor):

    class Context:
        def __init__(self, *, model, description, model_key, elements, processed, view):
            self.model = model
            self.description = description
            self.model_key = model_key
            self.elements = elements or []
            self.processed = processed
            self.view = view

        def __repr__(self):
            return (f"Context(model={self.model}, description={self.description}, model_key={self.model_key}, "
                   f"elements={self.elements}, processed={self.processed}, view={self.view})")

    def __init__(self):
        super().__init__()
        self._visited_contexts = {}
        self._context_stack = []
        self._model_key = 0
        self._current_context = None

    def reset(self):
        self._visited_contexts.clear()
        self._context_stack.clear()
        self._model_key = 0
        self._current_context = None

    def _shouldProcessDescription(self, description: MADescription) -> bool:
        return True

    def _transform_container(self, source: Any, description: MAContainer) -> Any:
        return source

    def _transform_element(self, source: Any, description: MAElementDescription) -> Any:
        return source

    def walkDescription(self, model: Any, description: MADescription) -> Any:
        raise NotImplementedError


class ModelReaderWalkerVisitor(MADescriptionWalkerVisitor):

    class Context(MADescriptionWalkerVisitor.Context):
        def __init__(self, *, model, description, model_key, elements=None, processed=False, view=None):
            super().__init__(model=model, description=description, model_key=model_key, elements=elements,
                             processed=processed, view=view)

    def get_model_key(self) -> int:  # technically key can be not int, but any hashable
        res = self._model_key
        self._model_key += 1
        return res

    def _process_cyclic_reference(self, ctx: Context) -> Any:
        raise CyclicReferenceError(ctx, f"Cyclic reference detected: {ctx}")

    def _process_duplicate_model(self, ctx: Context) -> Any:
        return ctx.view

    def walkDescription(self, model: Any, description: MADescription) -> Any:
        logger.info(f"{self.__class__.__name__}.walkDescription() called: "
                    f"model = {model.__class__.__name__} ({hex(id(model))}), "
                    f"description = {description.name} ({description.__class__.__name__})")
        if description is None:
            raise ValueError("Description cannot be None")
        if model == description.undefinedValue:
            return None

        model_id = id(model)
        if model_id in self._visited_contexts:
            logger.info(f"{self.__class__.__name__}.walkDescription(): "
                        f"model = {model.__class__.__name__} ({hex(id(model))}) was already visited")
            if len(self._visited_contexts) == 1:
                logger.info(f"{self.__class__.__name__}.walkDescription(): "
                            f"model = {model.__class__.__name__} ({hex(id(model))}) is the root model being visited "
                            f"via a to-one or single-option reference. We are good to go.")
            else:
                ctx = self._visited_contexts[model_id]
                if ctx.processed:
                    # if model was previously visited and processed - duplicate model reference
                    logger.info(f"{self.__class__.__name__}.walkDescription(): "
                                f"model = {model.__class__.__name__} ({hex(id(model))}) was already visited "
                                f"and processed")
                    return self._process_duplicate_model(ctx)
                else:
                    logger.info(f"{self.__class__.__name__}.walkDescription(): "
                                f"model = {model.__class__.__name__} ({hex(id(model))}): cyclic reference detected")
                    # if model was previously visited and not processed - cyclic reference
                    return self._process_cyclic_reference(ctx)

        logger.info(f"{self.__class__.__name__}.walkDescription(): "
                    f"model = {model.__class__.__name__} ({hex(id(model))}) was not visited before. Creating context.")
        context = self.Context(model=model, description=description, model_key=self.get_model_key())
        self._visited_contexts[model_id] = context
        logger.info(f"{self.__class__.__name__}.walkDescription(): Adding new context to context_stack: {context}")
        self._context_stack.append(context)
        self._current_context = self._context_stack[-1]
        self.visit(description)
        updated_context = self._context_stack.pop()
        updated_context.processed = True
        self._current_context = self._context_stack[-1] if self._context_stack else None
        logger.info(f"{self.__class__.__name__}.walkDescription(): "
                    f"model = {model.__class__.__name__} ({hex(id(model))}). Returning view: {updated_context.view}")
        return updated_context.view

    def visit(self, description: MADescription):
        logger.debug(f"{self.__class__.__name__}.visit() called with "
                     f"description = {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visit(): self._current_context: {self._current_context}")
        if self._shouldProcessDescription(description):
            super().visit(description)
        logger.debug(f"{self.__class__.__name__}.visit returning results for description "
                     f"= {description.name} ({description.__class__.__name__}): {self._current_context}")

    def visitContainer(self, description: MAContainer):
        logger.debug(f"{self.__class__.__name__}.visitContainer() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        self._current_context.elements = []
        self.visitAll(description.children)
        self._current_context.view = self._transform_container(self._current_context.elements, description)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        related_obj = MAModel.readUsingWrapper(self._current_context.model, description)
        if related_obj == description.undefinedValue:
            return None
        if related_obj is not None:
            ref_view = self.walkDescription(related_obj, description.reference)
        else:
            ref_view = None
        self._current_context.elements.append((description, ref_view))
        self._current_context.view = ref_view  # return only the view, in case it is the root model

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        related_objs = MAModel.readUsingWrapper(self._current_context.model, description)
        if related_objs == description.undefinedValue:
            return None
        if related_objs is not None:
            ref_views = []
            for obj in related_objs:
                ref_views.append(self.walkDescription(obj, description.reference))
            self._current_context.elements.append((description, ref_views))
            self._current_context.view = ref_views  # return only the views, in case it is the root model

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
        value = MAModel.readUsingWrapper(self._current_context.model, description)
        if value == description.undefinedValue:
            return None
        element_view = self._transform_element(value, description)
        self._current_context.elements.append((description, element_view))
        self._current_context.view = element_view  # return only the view, in case it is the root model


class ModelWriterWalkerVisitor(MADescriptionWalkerVisitor):

    class Context(MADescriptionWalkerVisitor.Context):
        def __init__(self, *, view, description, model_key=None, elements=None, processed=False, model=None):
            super().__init__(model=model, description=description, model_key=model_key, elements=elements,
                             processed=processed, view=view)

    def __init__(self):
        super().__init__()
        self._dto_factory = None

    def reset(self):
        super().reset()
        self._dto_factory = None

    def _process_duplicate_view(self, ctx_new: Context, ctx_old: Context) -> Any:
        raise DuplicateViewError(ctx_new, f"Duplicate view detected: {ctx_new} has same model_key as {ctx_old}")

    def walkDescription(self, view: Any, description: MADescription) -> Any:
        logger.info(f"{self.__class__.__name__}.walkDescription() called: "
                    f"view = {view.__class__.__name__} ({hex(id(view))}), "
                    f"description = {description.name} ({description.__class__.__name__})")
        if description is None:
            raise ValueError("Description cannot be None")

        context = self.Context(view=view, description=description)

        logger.info(f"{self.__class__.__name__}.walkDescription(): Adding new context to context_stack: {context}")
        self._context_stack.append(context)
        self._current_context = self._context_stack[-1]
        self.visit(description)
        updated_context = self._context_stack.pop()
        updated_context.processed = True
        self._current_context = self._context_stack[-1] if self._context_stack else None

        model_key = updated_context.model_key

        if model_key is not None:
            if model_key in self._visited_contexts:
                logger.info(f"{self.__class__.__name__}.walkDescription(): "
                            f"model with key {model_key} was already visited")
                updated_context = self._process_duplicate_view(updated_context, self._visited_contexts[model_key])
            self._visited_contexts[model_key] = updated_context

        logger.info(f"{self.__class__.__name__}.walkDescription(): "
                    f"model with key {model_key}. Returning model: {updated_context.model}")
        return updated_context.model

    @staticmethod
    def default_dto_factory(description: MAContainer) -> Any:
        c = description.kind
        if c is None:
            raise MAKindError(description, 'Kind is not defined to make an instance of the described entity')
        return c()

    def _get_model_by_key(self, key: int) -> Any:  # symmetrically to ModelReaderWalkerVisitor - key is int
        # try to find the model by key, if not found raise KeyError
        if key in self._visited_contexts:
            return self._visited_contexts[key].model
        for ctx in self._context_stack:
            if ctx.model_key == key:
                return ctx.model
        raise KeyError(f"Model with key {key} not found in visited_contexts")

    def _get_element_view(self, description: MAElementDescription) -> Any:
        return next(
            filter(lambda x: x[0] == description, self._current_context.elements),
            (description, description.undefinedValue)
            )[1]

    def visit(self, description: MADescription):
        logger.debug(f"{self.__class__.__name__}.visit() called with "
                     f"description = {description.name} ({description.__class__.__name__})")
        logger.debug(f"{self.__class__.__name__}.visit(): self._current_context: {self._current_context}")
        if self._shouldProcessDescription(description):
            super().visit(description)
        logger.debug(f"{self.__class__.__name__}.visit returning results for description "
                     f"= {description.name} ({description.__class__.__name__}): {self._current_context}")

    def visitContainer(self, description: MAContainer):
        logger.debug(f"{self.__class__.__name__}.visitContainer() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        dto_factory = self._dto_factory if self._dto_factory else self.default_dto_factory
        self._current_context.model = dto_factory(description)
        self._current_context.elements = self._transform_container(self._current_context.view, description)
        self.visitAll(description.children)

    def visitToOneRelationDescription(self, description: MAToOneRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToOneRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        if self._current_context.model is not None:
            related_view = self._get_element_view(description)
        else:  # parse and return only the element, in case it is the root view
            related_view = self._current_context.view
        if related_view == description.undefinedValue:
            related_obj = description.undefinedValue
        else:
            related_obj = self.walkDescription(related_view, description.reference)
        if self._current_context.model is not None:
            MAModel.writeUsingWrapper(self._current_context.model, description, related_obj)
        else:
            self._current_context.model = related_obj  # return only the element, in case it is the root view

    def visitToManyRelationDescription(self, description: MAToManyRelationDescription):
        logger.debug(f"{self.__class__.__name__}.visitToManyRelationDescription() called with "
                     f"description {description.name} ({description.__class__.__name__})")
        if self._current_context.model is not None:
            related_views = self._get_element_view(description)
        else:  # parse and return only the element, in case it is the root view
            related_views = self._current_context.view
        if related_views == description.undefinedValue:
            related_objs = description.undefinedValue
        elif related_views is None:
            related_objs = None
        else:
            related_objs = []
            for view in related_views:
                related_objs.append(self.walkDescription(view, description.reference))
        if self._current_context.model is not None:
            MAModel.writeUsingWrapper(self._current_context.model, description, related_objs)
        else:
            self._current_context.model = related_objs  # return only the elements, in case it is the root view

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
        if self._current_context.model is not None:
            element_view = self._get_element_view(description)
            element_value = self._transform_element(element_view, description)
            MAModel.writeUsingWrapper(self._current_context.model, description, element_value)
        else:
            # parse and return only the element, in case it is the root view
            element_value = self._transform_element(self._current_context.view, description)
            self._current_context.model = element_value


class MAReferencedDataHumanReadableSerializer(ModelReaderWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._json_writer = MAValueJsonWriter()

    def _process_cyclic_reference(self, ctx: ModelReaderWalkerVisitor.Context) -> Any:
        return ctx.model_key

    def _process_duplicate_model(self, ctx: ModelReaderWalkerVisitor.Context) -> Any:
        return ctx.model_key

    def _shouldProcessDescription(self, description: MADescription) -> bool:
        if not description.isVisible():
            return False
        if (isinstance(description.accessor, MAPluggableAccessor)
                and not description.accessor.canRead(None)):  # MAPluggableAccessor canRead does not depend on model
            return False
        return True

    def _transform_container(self, source: Any, description: MAContainer) -> Any:
        obj_dict = {
            "-x-magritte-class": self._current_context.model.__class__.__name__,
            "-x-magritte-key": self._current_context.model_key,
        }
        obj_dict.update({desc.name: value for desc, value in source})
        return obj_dict

    def _transform_element(self, source: Any, description: MAElementDescription) -> Any:
        return self._json_writer.write_json(self._current_context.model, description)

    def dumpHumanReadable(self, model: Any, description: MADescription):
        logger.debug(f"{self.__class__.__name__}.dumpHumanReadable(): "
                     f"model {model.__class__.__name__} ({hex(id(model))}), "
                     f"description {description.name} ({description.__class__.__name__})")
        self.reset()
        return self.walkDescription(model, description)

    def serializeHumanReadable(self, model: Any, description: MADescription, indent=None):
        logger.debug(f"{self.__class__.__name__}.serializeHumanReadable(): "
                     f"model {model.__class__.__name__} ({hex(id(model))}), "
                     f"description {description.name} ({description.__class__.__name__})")
        return json.dumps(self.dumpHumanReadable(model, description), indent=indent)


class MAReferencedDataHumanReadableDeserializer(ModelWriterWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._dto_factory = None
        self._json_reader = MAValueJsonReader()

    def _shouldProcessDescription(self, description: MADescription) -> bool:
        if not description.isVisible() or description.isReadOnly():
            return False
        if (isinstance(description.accessor, MAPluggableAccessor)
                and not description.accessor.canWrite(None)):  # MAPluggableAccessor canWrite does not depend on model
            return False
        return True

    def _transform_container(self, source: Any, description: MAContainer) -> Any:
        elements = []
        for elem_desc in description.children:
            elem_name = elem_desc.name
            elem_value = source.get(elem_name, elem_desc.undefinedValue)
            elements.append((elem_desc, elem_value))
        return elements

    def _transform_element(self, source: Any, description: MAElementDescription) -> Any:
        return self._json_reader.read_json(None, source, description)

    def visitContainer(self, description: MAContainer):
        if not isinstance(self._current_context.view, dict):
            self._current_context.model = self._get_model_by_key(self._current_context.view)
            return
        if '-x-magritte-key' not in self._current_context.view:
            raise ValueError(f"'-x-magritte-key' not found in view: {self._current_context.view}")
        self._current_context.model_key = self._current_context.view['-x-magritte-key']
        super().visitContainer(description)

    def instantiateHumanReadable(self, dump: Any, description: MADescription, dto_factory: callable=None) -> Any:
        logger.debug(f"{self.__class__.__name__}.instantiateHumanReadable(): "
                     f"dump {dump}, description {description.name} ({description.__class__.__name__})")
        if dto_factory is None:
            self._dto_factory = self.default_dto_factory
        model = self.walkDescription(dump, description)
        return model

    def deserializeHumanReadable(self, serialized_str: str, description: MADescription, dto_factory: callable=None) -> Any:
        logger.debug(f"{self.__class__.__name__}.deserializeHumanReadable(): "
                     f"serialized_str {serialized_str}, "
                     f"description {description.name} ({description.__class__.__name__})")
        dump = json.loads(serialized_str)
        return self.instantiateHumanReadable(dump, description, dto_factory)


class MAReferencedDataPrinter(ModelReaderWalkerVisitor):
    def __init__(self):
        super().__init__()
        self._indent = '= '
        self._level_prefix = ''
        self._elem_prefix = '- '
        self._c_prefix = ''
        self._e_prefix = ''

    def _process_cyclic_reference(self, ctx: ModelReaderWalkerVisitor.Context) -> Any:
        return f"<cyclic ref>"

    def print(self, model: Any, description: MADescription):
        self.reset()
        res = self.walkDescription(model, description)
        print("======================================================")
        print(res)
        print("======================================================")

    def _transform_container(self, source: Any, description: MAContainer) -> Any:
        self._level_prefix = self._indent * len(self._context_stack)
        self._c_prefix = self._level_prefix
        self._e_prefix = self._level_prefix + self._elem_prefix
        header = f"{self._c_prefix}Object described by {description.name} ({description.__class__.__name__}): "
        res = []
        for elem_desc, elem_value in source:
            if isinstance(elem_value, list):
                res.append(f"{self._e_prefix}{elem_desc.name}:")
                for elem in elem_value:
                    if elem == "<cyclic ref>":
                        elem_res = f"{self._c_prefix + self._indent}{elem}"
                    else:
                        elem_res = f"{elem}"
                    res.append(elem_res)
            else:
                res.append(f"{self._e_prefix}{elem_desc.name}: {elem_value}")
        return header + "\n" +  "\n".join(res)


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
        def __init__(self, name=None):
            self.id = 0
            self.name = name
            self.children = []

        def __repr__(self):
            return f"Parent({self.name})"

    class Child:
        def __init__(self, nick=''):
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

    parent2 = Parent("Jane")

    child2 = Child("Jenny")
    child2.parent = parent2

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
    # print(serializer.dumpHumanReadable(child.parent, child_parent_desc))
    # print(serializer.serializeHumanReadable(child.parent, child_parent_desc, indent=2))

    # reader = ModelReaderWalkerVisitor()
    # writer = ModelWriterWalkerVisitor()
    # child_view = reader.walkDescription(child2, child_desc)
    # print(child_view)
    # new_child = writer.walkDescription(child_view, child_desc)
    # print(new_child)
    # print(new_child.parent)

    deserializer = MAReferencedDataHumanReadableDeserializer()

    # child_dict = {'-x-magritte-key': 0, 'nick': 'Jacky', 'parent': {'-x-magritte-key': 1, 'name': 'Jack', 'children': []}}
    # new_child = deserializer.instantiateHumanReadable(child_dict, child_desc)
    # print(new_child)
    # print(new_child.parent)
    # print(new_child.parent.children)

    # child_nick = 'Jacky'
    # child_dict = {'-x-magritte-key': 0, 'nick': 'Jacky', 'parent': {'-x-magritte-key': 1, 'name': 'Jack', 'children': []}}
    # nick_desc = child_desc['nick']
    # str_instantiated = deserializer.instantiateHumanReadable('Jacky', nick_desc)
    # print(str_instantiated)

    # parent_desc = child_desc['parent']
    # parent_dict = {'-x-magritte-key': 1, 'name': 'Jack', 'children': []}
    # parent_instantiated = deserializer.instantiateHumanReadable(parent_dict, parent_desc)
    # print(parent_instantiated)
    # print(parent_instantiated.children)

    # children_desc = parent_desc['children']
    # children_dict = [{'-x-magritte-key': 0, 'nick': 'Jacky', 'parent': {'-x-magritte-key': 1, 'name': 'Jack', 'children': [0]}}]
    # children_instantiated = deserializer.instantiateHumanReadable(children_dict, children_desc)
    # print(children_instantiated)
    # print(children_instantiated[0])
    # print(children_instantiated[0].parent)

    # print(host)
    # host_dict = serializer.dumpHumanReadable(host, host_desc)
    # print(host_dict)
    # new_host = deserializer.instantiateHumanReadable(host_dict, host_desc)
    # print(new_host)
    # new_host_dict = serializer.dumpHumanReadable(new_host, host_desc)
    # print(new_host_dict)
    # host_str = serializer.serializeHumanReadable(host, host_desc)
    # print(host_str)
    # new_host = deserializer.deserializeHumanReadable(host_str, host_desc)
    # print(new_host)
    # new_host_str = serializer.serializeHumanReadable(new_host, host_desc)
    # print(new_host_str)

    subscriptionPlanDescription = desc_provider.description_for("SubscriptionPlan")
    subscriptionPlanWithoutPriceJson = '{"-x-magritte-key": 1, "name": "Free"}'
    subscriptionPlanWithoutPriceDeserialized = deserializer.deserializeHumanReadable(subscriptionPlanWithoutPriceJson, subscriptionPlanDescription)
    print(subscriptionPlanWithoutPriceDeserialized.price)
