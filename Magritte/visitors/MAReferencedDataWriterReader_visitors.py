
from typing import Any, Union
import json
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.MAModel_class import MAModel
from Magritte.visitors.MAJsonWriter_visitors import MAValueJsonReader, MAValueJsonWriter


class MADescriptorWalker:

    class _WalkerVisitor(MAVisitor):

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
            pass

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
            (source_index, was_added,) = self._addSourceOnce(aSource)
            self._contexts_by_source_id[source_index] = self._context
            self._walkFromCurrent()
            return self._contexts


    class _DumpModelWalkerVisitor(_WalkerVisitor):
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

    class _InstaniateModelWalkerVisitor(_WalkerVisitor):
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
                value = subcontext_dump_matching_name['value']
            #MAModel.writeUsingWrapper(model, description, value)
            jsonReader = MAValueJsonReader()
            jsonReader.read_json(model, value, description)
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

"""
    def dumpModel(self, aModel: Any, aDescription: MADescription, doReadElementValues=False):
        walker = self.__class__._DumpModelWalkerVisitor()
        return walker.dumpModel(aModel, aDescription, doReadElementValues)

    def instaniateModel(self, contexts_dump, root_dump_index, description, dto_factory):
        walker = self.__class__._InstaniateModelWalkerVisitor()
        return walker.instaniateModel(contexts_dump, root_dump_index, description, dto_factory)
"""

class MAReferencedDataHumanReadableSerializer:

    class _HumanReadableDumpModelWalkerVisitor(MADescriptorWalker._DumpModelWalkerVisitor):
        def __init__(self):
            super().__init__()
            self._jsonWriter = MAValueJsonWriter()

        def _clear(self):
            super()._clear()
            self._dumpResultPerContextIndex = {}
            self._dumpEmittedPerContentIndex = {}

        def _emitDumpOnce(self, context):
            context_index = context.context_index
            ref_count = self._dumpEmittedPerContentIndex[context_index] if context_index in self._dumpEmittedPerContentIndex else 0
            ref_count += 1
            self._dumpEmittedPerContentIndex[context_index] = ref_count
            if ref_count == context.ref_count:
                return self._dumpResultPerContextIndex[context.context_index]
            else:
                return context.context_index

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
    class _HumanReadableInstaniateModelWalkerVisitor(MADescriptorWalker._InstaniateModelWalkerVisitor):
        def instaniateModelHumanReadable(self, dump, description, dto_factory):
            if dump is None:
                return None
            return None

    @staticmethod
    def default_dto_factory(description):
        c = description.kind
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
    descriptorWalker = MADescriptorWalker()
    #descriptorWalker.dumpModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[0]
    portDescriptor = TestModelDescriptor.description_for("Port")
    #descriptorWalker.dumpModel(port, portDescriptor)
    #testVisitor._walker._dbg_print()

    serializer = MAReferencedDataHumanReadableSerializer()
    serialized_str = serializer.serializeHumanReadable(host, hostDescriptor)
    print(serialized_str)

    serialized_str = serializer.serializeHumanReadable(port, portDescriptor)
    print(serialized_str)

    serialized_str = serializer.serializeHumanReadable(host, hostDescriptor.children[0])
    print(serialized_str)

    def custom_dto_factory(description):
        if description.name == 'Host': return Host()
        if description.name == 'Port': return Port()
        return None
    deserializer = MAReferencedDataHumanReadableDeserializer()
    dto = deserializer.deserializeHumanReadable(serialized_str, hostDescriptor, dto_factory=custom_dto_factory)
    print(dto)

