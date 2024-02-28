
from typing import Any, Union
import json
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.MAModel_class import MAModel
from Magritte.visitors.MAJsonWriter_visitors import MAValueJsonReader, MAValueJsonWriter
from Magritte.errors.MAKindError import MAKindError


class MADescriptorWalker:

    class WalkerVisitor(MAVisitor):

        class _Context:
            parent_context = None
            context_index: int = None
            source: Any = None                          # Arbitrary object reference related to the context. Used to get targets from somewhere to break cyclic references and extract subsources for subcontexts.
            description: MADescription = None
            subcontexts: list = None
            ref_count: int = 1

        def __init__(self):
            self._contexts = None
            self._contexts_by_source_id = None
            self._sources = None
            self._sources_by_source_index = None
            self._source_indices_by_identifier = None
            self._source_indices_by_context_index = None
            self._clear()

        def _clear(self):
            self._contexts = []
            self._contexts_by_source_id = {}
            self._sources = []
            self._sources_by_source_index = {}
            self._source_indices_by_identifier = {}
            self._source_indices_by_context_index = {}

        def _createEmptyContext(self):
            context_index = len(self._contexts)
            self._context = self.__class__._Context()
            self._contexts.append(self._context)
            self._context.context_index = context_index
            return self._context

        def _addSource(self, source):
            source_index = len(self._sources)
            self._sources.append(source)
            self._sources_by_source_index[source_index] = source
            return source_index

        def _addSourceOnce(self, source):
            identifier = id(source)
            if identifier in self._source_indices_by_identifier:
                was_added = False
                source_index = self._source_indices_by_identifier[identifier]
            else:
                was_added = True
                source_index = len(self._sources)
                self._sources.append(source)
                self._source_indices_by_identifier[identifier] = source_index
                self._sources_by_source_index[source_index] = source
            return (source_index, was_added,)

        def _walkFromCurrent(self):
            description = self._context.description
            if not description.visible:
                return
            description.acceptMagritte(self)

        def visitElementDescription(self, description: MADescription):
            context = self._context
            source = self.processElementDescriptionContext(context, description)
            source_index = self._addSource(source)
            self._source_indices_by_context_index[context.context_index] = source_index

        def visitContainer(self, description: MAContainer):
            context = self._context
            self.processContainerContext(context, description)
            context.subcontexts = []
            for subdescription in description:
                subcontext = self._createEmptyContext()
                subcontext.parent_context = context
                context.subcontexts.append(subcontext)
                subcontext.source = context.source
                subcontext.description = subdescription
                self._walkFromCurrent()

        def visitToOneRelationDescription(self, description: MAReferenceDescription):
            context = self._context
            subsource = self.processToOneRelationContext(context, description)
            (subsource_index, was_added,) = self._addSourceOnce(subsource)
            if was_added:
                subcontext = self._createEmptyContext()
                subcontext.parent_context = context
                subcontext.source = subsource
                subcontext.description = description.reference
                self._contexts_by_source_id[subsource_index] = subcontext
                self._walkFromCurrent()
            else:
                subcontext = self._contexts_by_source_id[subsource_index]
                subcontext.ref_count += 1
            context.subcontexts = [subcontext]

        def visitToManyRelationDescription(self, description):
            context = self._context
            subsources = self.processToManyRelationContext(context, description)
            context.subcontexts = []
            for subsource in subsources:
                (subsource_index, was_added,) = self._addSourceOnce(subsource)
                if was_added:
                    subcontext = self._createEmptyContext()
                    subcontext.parent_context = context
                    subcontext.source = subsource
                    subcontext.description = description.reference
                    self._contexts_by_source_id[subsource_index] = subcontext
                    self._walkFromCurrent()
                else:
                    subcontext = self._contexts_by_source_id[subsource_index]
                    subcontext.ref_count += 1
                context.subcontexts.append(subcontext)

        def processContainerContext(self, context, description):
            (source_index, was_added,) = self._addSourceOnce(self._context.source)
            self._contexts_by_source_id[source_index] = self._context

        def processElementDescriptionContext(self, context, description):
            return None

        def processToOneRelationContext(self, context, description):
            return None

        def processToManyRelationContext(self, context, description):
            return []

        def walkDescription(self, aSource: Any, aDescription: MADescription):
            self._clear()
            self._createEmptyContext()
            self._context.source = aSource
            self._context.description = aDescription
            self._walkFromCurrent()
            return self._contexts


    class DumpModelWalkerVisitor(WalkerVisitor):
        def __init__(self):
            super().__init__()
            self._doReadElementValues = None

        def _dbg_print(self):
            printed_contexts = set()
            def printContext(sPrefix: str, aContext):
                context_index = aContext.context_index
                printed_contexts.add(context_index)
                print(f'{sPrefix}Context {context_index}, {aContext.description.name}, referenced {aContext.ref_count} time(s):')
                subPrefix = f'{sPrefix}  '
                if aContext.subcontexts is None:
                    print(f'{subPrefix}Value of {aContext.description.name}, {self._sources[self._source_indices_by_context_index[aContext.context_index]]}')
                else:
                    for subcontext in aContext.subcontexts:
                        subcontext_index = subcontext.context_index
                        if subcontext_index in printed_contexts:
                            print(f'{subPrefix}Context {subcontext_index}, {subcontext.description.name} // already printed')
                        else:
                            printContext(subPrefix, subcontext)

            printContext('', self._contexts[0])

        def processElementDescriptionContext(self, context, description):
            if self._doReadElementValues:
                value = MAModel.readUsingWrapper(context.source, context.description)
                return value
            else:
                return None

        def processToOneRelationContext(self, context, description):
            model = context.source
            value = MAModel.readUsingWrapper(model, description)
            return value

        def processToManyRelationContext(self, context, description):
            values = MAModel.readUsingWrapper(context.source, description)
            return values

        def dumpModel(self, aModel: Any, aDescription: MADescription, doReadElementValues):
            self._doReadElementValues = doReadElementValues
            return self.walkDescription(aModel, aDescription)

    class InstaniateModelWalkerVisitor(WalkerVisitor):  # Not used for now
        def __init__(self):
            super().__init__()
            self._contexts_dump = None
            self._dtos_by_dump_index = None
            self._dto_factory = None

        def _clear(self):
            super()._clear()
            self._dtos_by_dump_index = {}

        #def processContainerContext(self, context, description):
        #    if context.context_index in self._dtos_by_context_index: return

        def _getOrCreateDTO(self, dump_index, dto_description):
            if dump_index not in self._dtos_by_dump_index:
                dto = self._dto_factory(dto_description)
                self._dtos_by_dump_index[dump_index] = dto
            return self._dtos_by_dump_index[dump_index]

        def _findMatchingSubcontextDump(self, context, description):
            name = description.name
            dump_index = context.source
            dump = self._contexts_dump[dump_index]
            subcontext_dump_index_matching_name = None
            for subcontext_dump_index in dump['subcontext_indices']:
                subcontext_dump = self._contexts_dump[subcontext_dump_index]
                if subcontext_dump['name'] == name:
                    subcontext_dump_index_matching_name = subcontext_dump_index
                    break
            return subcontext_dump_index_matching_name

        def processElementDescriptionContext(self, context, description):
            model = self._getOrCreateDTO(context.source, context.parent_context.description)
            subcontext_dump_index_matching_name = self._findMatchingSubcontextDump(context, description)
            if subcontext_dump_index_matching_name is None:
                value = description.undefinedValue
            else:
                subcontext_dump_matching_name = self._contexts_dump[subcontext_dump_index_matching_name]
                subcontext_dump = subcontext_dump_matching_name['value']
                jsonReader = MAValueJsonReader()
                value = jsonReader.read_json(None, subcontext_dump, description)
            MAModel.writeUsingWrapper(model, description, value)
            return subcontext_dump_index_matching_name

        def processToOneRelationContext(self, context, description):
            model = self._getOrCreateDTO(context.source, context.parent_context.description)
            subcontext_dump_index_matching_name = self._findMatchingSubcontextDump(context, description)
            if subcontext_dump_index_matching_name is None:
                value = description.undefinedValue
                subcontext_dump_reference_index = None
            else:
                subcontext_dump_matching_name = self._contexts_dump[subcontext_dump_index_matching_name]
                subcontext_dump_reference_index = subcontext_dump_matching_name['subcontext_indices'][0]
                #subcontext_dump_reference = self._contexts_dump[subcontext_dump_reference_index]
                if subcontext_dump_reference_index in self._dtos_by_dump_index:
                    value = self._dtos_by_dump_index[subcontext_dump_reference_index]
                else:
                    value = None
            MAModel.writeUsingWrapper(model, description, value)
            return subcontext_dump_reference_index

        def processToManyRelationContext(self, context, description):
            model = self._getOrCreateDTO(context.source, context.parent_context.description)
            relations_list = MAModel.readUsingWrapper(model, description)
            subcontext_dump_index_matching_name = self._findMatchingSubcontextDump(context, description)
            if subcontext_dump_index_matching_name is None:
                subcontext_dump_indices = []
                relations_list.clear()
                if description.undefinedValue is not None:
                    relations_list.extend(description.undefinedValue)
            else:
                subcontext_dump_matching_name = self._contexts_dump[subcontext_dump_index_matching_name]
                subcontext_dump_indices = []
                for subcontext_dump_index in subcontext_dump_matching_name['subcontext_indices']:
                    #subcontext_dump = self._contexts_dump[subcontext_dump_index]
                    submodel = self._getOrCreateDTO(subcontext_dump_index, description.reference)
                    subcontext_dump_indices.append(subcontext_dump_index)
                    relations_list.append(submodel)
            return subcontext_dump_indices

        def instaniateModel(self, contexts_dump, root_dump_index, description, dto_factory):
            self._contexts_dump = contexts_dump
            self._dto_factory = dto_factory
            self.walkDescription(root_dump_index, description)
            if root_dump_index in self._dtos_by_dump_index:
                return self._dtos_by_dump_index[root_dump_index]
            else:
                return None


class MAReferencedDataHumanReadableSerializer:

    class _HumanReadableDumpModelWalkerVisitor(MADescriptorWalker.DumpModelWalkerVisitor):
        def __init__(self):
            super().__init__()
            self._jsonWriter = MAValueJsonWriter()

        def _clear(self):
            super()._clear()
            self._dumpResultPerContextIndex = {}
            #self._dumpEmittedPerContentIndex = {}

        def _emitDumpOnce(self, context):
            context_index = context.context_index
            if context_index in self._dumpResultPerContextIndex:
                return self._dumpResultPerContextIndex[context_index]
            else:
                return context_index

        def visitElementDescription(self, aDescription):
            context = self._context
            super().visitElementDescription(aDescription)
            dumpResult = self._jsonWriter.write_json(context.source, aDescription)
            self._dumpResultPerContextIndex[context.context_index] = dumpResult
            #print(f'processElementDescriptionContext {aDescription.name} {dumpResult}')

        def visitContainer(self, aDescription):
            context = self._context
            super().visitContainer(aDescription)
            dumpResult = {'_key': context.context_index}
            self._dumpResultPerContextIndex[context.context_index] = dumpResult
            for subcontext in context.subcontexts:
                if subcontext.description.visible:
                    dumpResult[subcontext.description.name] = self._dumpResultPerContextIndex[subcontext.context_index]
            #print(f'processContainerContext {aDescription.name} {dumpResult}')

        def visitToOneRelationDescription(self, aDescription):
            context = self._context
            super().visitToOneRelationDescription(aDescription)
            subcontext = context.subcontexts[0]
            dumpResult = self._emitDumpOnce(subcontext)
            self._dumpResultPerContextIndex[context.context_index] = dumpResult
            #print(f'processToOneRelationContext {aDescription.name} {dumpResult}')

        def visitToManyRelationDescription(self, aDescription):
            context = self._context
            super().visitToManyRelationDescription(aDescription)
            dumpResult = []
            self._dumpResultPerContextIndex[context.context_index] = dumpResult
            for subcontext in context.subcontexts:
                subResult = self._emitDumpOnce(subcontext)
                dumpResult.append(subResult)
            #print(f'processToManyRelationContext {aDescription.name} {dumpResult}')

        def dumpModelHumanReadable(self, aModel: Any, aDescription: MADescription):
            self.dumpModel(aModel, aDescription, doReadElementValues=False)
            return self._dumpResultPerContextIndex[0] if 0 in self._dumpResultPerContextIndex else None

    def dumpHumanReadable(self, model: Any, description: MADescription) -> Any:
        descriptorWalker = self.__class__._HumanReadableDumpModelWalkerVisitor()
        return descriptorWalker.dumpModelHumanReadable(model, description)

    def serializeHumanReadable(self, model: Any, description: MADescription) -> str:
        dump = self.dumpHumanReadable(model, description)
        serialized_str = json.dumps(dump)
        return serialized_str


"""
class MAReferencedDataDeserializer:

    @staticmethod
    def default_dto_factory(description):
        c = description.kind
        return c()

    def instaniate(self, dump_dict: dict, description: MADescription, dto_factory=default_dto_factory):
        descriptorWalker = MADescriptorWalker()
        contexts = dump_dict['contexts']
        root_dump_index = dump_dict['root_context_index']
        if root_dump_index is None:
            model = None
        else:
            model = descriptorWalker.instaniateModel(contexts, root_dump_index, description, dto_factory)
        return model

    def deserialize(self, serialized_str: str, description: MADescription, dto_factory=default_dto_factory) -> str:
        dump_dict = json.loads(serialized_str)
        return self.instaniate(dump_dict, description, dto_factory)
"""

class MAReferencedDataHumanReadableDeserializer:

    class _HumanReadableInstaniateModelWalkerVisitor(MADescriptorWalker.WalkerVisitor):

        def __init__(self):
            super().__init__()
            self._jsonReader = MAValueJsonReader()
            self._dto_factory = None

        def _clear(self):
            super()._clear()
            self._dtos_by_key = {}
            self._values_by_dump_id = {}
            self._dumps_by_key = {}

        def _getOrCreateDTO(self, dump, dto_description):
            key = dump['_key']
            if key not in self._dtos_by_key:
                dto = self._dto_factory(dto_description)
                self._dtos_by_key[key] = dto
                self._dumps_by_key[key] = dump
            return self._dtos_by_key[key]

        def _getParentModel(self, context):
            if context.parent_context is None:
                # todo: conception of virtual root model?
                return None
            else:
                return self._getOrCreateDTO(context.source, context.parent_context.description)

        def _getDTOdumpByKey(self, dump):
            if isinstance(dump, int):
                return self._dumps_by_key[dump]
            return dump

        def _addValueForDump(self, dump, value):
            self._values_by_dump_id[id(dump)] = value

        def _findMatchingSubcontextDump(self, context, description):
            name = description.name
            dump = context.source
            if name in dump:
                return (True, dump[name],)
            return (False, None,)

        def processElementDescriptionContext(self, context, description):
            model = self._getParentModel(context)
            if model is None:  # The MAElementDescription serialized data is the root model without enclosing DTO - special handling
                dump = context.source
                value = self._jsonReader.read_json(None, dump, description)
                self._addValueForDump(dump, value)
            else:
                found, subcontext_dump = self._findMatchingSubcontextDump(context, description)
                if found:
                    value = self._jsonReader.read_json(None, subcontext_dump, description)
                else:
                    value = description.undefinedValue
                MAModel.writeUsingWrapper(model, description, value)
                #self._addValueForDump(subcontext_dump, value)
            return None

        def processToOneRelationContext(self, context, description):
            model = self._getParentModel(context)
            found, subcontext_dump_or_key = self._findMatchingSubcontextDump(context, description)
            if found:
                subcontext_dump = self._getDTOdumpByKey(subcontext_dump_or_key)
                submodel = self._getOrCreateDTO(subcontext_dump, description.reference)
            else:
                subcontext_dump = None
                submodel = description.undefinedValue
            self._addValueForDump(subcontext_dump, submodel)
            MAModel.writeUsingWrapper(model, description, submodel)
            return subcontext_dump

        def processToManyRelationContext(self, context, description):
            model = self._getParentModel(context)
            if model is None:  # The MAToManyRelationDescription serialized data is the root model without enclosing DTO - special handling
                dump = context.source
                relations_list = []
                self._addValueForDump(dump, relations_list)
                found = True
                subcontext_dump = dump
            else:
                relations_list = MAModel.readUsingWrapper(model, description)
                found, subcontext_dump = self._findMatchingSubcontextDump(context, description)
            if found:
                subcontext_dumps = []
                for relation_dump_or_key in subcontext_dump:
                    relation_dump = self._getDTOdumpByKey(relation_dump_or_key)
                    submodel = self._getOrCreateDTO(relation_dump, description.reference)
                    subcontext_dumps.append(relation_dump)
                    self._addValueForDump(relation_dump, submodel)
                    relations_list.append(submodel)
            else:
                subcontext_dumps = []
                relations_list.clear()
                if description.undefinedValue is not None:
                    relations_list.extend(description.undefinedValue)
            return subcontext_dumps

        def instaniateModelHumanReadable(self, dump, description, dto_factory):
            if dump is None:
                return None
            self._dto_factory = dto_factory
            self.walkDescription(dump, description)
            root_dump_id = id(dump)
            if root_dump_id in self._values_by_dump_id:
                return self._values_by_dump_id[root_dump_id]
            return None


    @staticmethod
    def default_dto_factory(description):
        c = description.kind
        if c is None:
            raise MAKindError(description, 'Kind is not defined to make an instance of the described entity')
        return c()

    def instaniateHumanReadable(self, dump: Any, description: MADescription, dto_factory=default_dto_factory) -> Any:
        descriptorWalker = self.__class__._HumanReadableInstaniateModelWalkerVisitor()
        model = descriptorWalker.instaniateModelHumanReadable(dump, description, dto_factory)
        return model

    def deserializeHumanReadable(self, serialized_str: str, description: MADescription, dto_factory=default_dto_factory) -> Any:
        dump = json.loads(serialized_str)
        return self.instaniateHumanReadable(dump, description, dto_factory)


if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port

    provider = TestEnvironmentProvider()
    host = provider.hosts[0]
    hostDescriptor = TestModelDescriptor.description_for("Host")
    #descriptorWalker = MADescriptorWalker()
    #descriptorWalker.dumpModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[5]
    portDescriptor = TestModelDescriptor.description_for("Port")
    #descriptorWalker.dumpModel(port, portDescriptor)
    #testVisitor._walker._dbg_print()

    ipDescriptor = hostDescriptor.children[0]
    portsDescriptor = hostDescriptor.children[1]

    #host.ports = [host.ports[0]]

    serializer = MAReferencedDataHumanReadableSerializer()
    serialized_str_h = serializer.serializeHumanReadable(host, hostDescriptor)
    print(serialized_str_h)

    serialized_str_p = serializer.serializeHumanReadable(port, portDescriptor)
    print(serialized_str_p)

    serialized_str_ip = serializer.serializeHumanReadable(host, ipDescriptor)
    print(serialized_str_ip)

    serialized_str_ports = serializer.serializeHumanReadable(host, portsDescriptor)
    print(serialized_str_ports)

    deserializer = MAReferencedDataHumanReadableDeserializer()

    dto_h = deserializer.deserializeHumanReadable(serialized_str_h, hostDescriptor)
    print(dto_h)

    dto_p = deserializer.deserializeHumanReadable(serialized_str_p, portDescriptor)
    print(dto_p)

    dto_ip = deserializer.deserializeHumanReadable(serialized_str_ip, ipDescriptor)
    print(dto_ip)

    dto_ports = deserializer.deserializeHumanReadable(serialized_str_ports, portsDescriptor)
    print(dto_ports)
    print(len(host.ports), len(dto_ports))