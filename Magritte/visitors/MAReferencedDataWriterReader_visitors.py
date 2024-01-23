
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
            return super().walkDescription(aModel, aDescription)

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


    def dumpModel(self, aModel: Any, aDescription: MADescription, doReadElementValues=False):
        walker = self.__class__._DumpModelWalkerVisitor()
        return walker.dumpModel(aModel, aDescription, doReadElementValues)

    def instaniateModel(self, contexts_dump, root_dump_index, description, dto_factory):
        walker = self.__class__._InstaniateModelWalkerVisitor()
        return walker.instaniateModel(contexts_dump, root_dump_index, description, dto_factory)


class MAReferencedDataSerializer:

    class _ElementDescriptionJsonWriterVisitor(MAVisitor):
        def __init__(self, aModel):
            self.model = aModel
            self.isElementDescription = False
            self.jsonValue = None

        def visitElementDescription(self, aDescription):
            self.isElementDescription = True
            jsonWriter = MAValueJsonWriter()
            self.result = jsonWriter.write_json(self.model, aDescription)

    def _walkFromCurrent(self, contexts, context):
        context_index_str = str(context.context_index)
        if context_index_str in contexts:
            return
        result = { 'name': context.description.name }
        contexts[context_index_str] = result

        if context.subcontexts is None:
            jsonWriterVisitor = self.__class__._ElementDescriptionJsonWriterVisitor(context.source)
            context.description.acceptMagritte(jsonWriterVisitor)
            result['value'] = jsonWriterVisitor.result if jsonWriterVisitor.isElementDescription else None
            # result['value_index'] = context.value_index
            # if jsonElementDescriptionEncoder.isElementDescription:
            #    values[context.value_index] = jsonElementDescriptionEncoder.result
        else:
            subcontext_indices = []
            for subcontext in context.subcontexts:
                subcontext_indices.append(str(subcontext.context_index))
                self._walkFromCurrent(contexts, subcontext)
            result['subcontext_indices'] = subcontext_indices

    def dump(self, model: Any, description: MADescription) -> dict:
        descriptorWalker = MADescriptorWalker()
        contexts = descriptorWalker.dumpModel(model, description)
        result = { 'contexts': {}, 'root_context_index': None }
        if len(contexts) > 0:
            result['root_context_index'] = '0'
            self._walkFromCurrent(result['contexts'], contexts[0])
        return result

    def serialize(self, model: Any, description: MADescription) -> str:
        dump_dict = self.dump(model, description)
        serialized_str = json.dumps(dump_dict)
        return serialized_str



class MAReferencedDataHumanReadableSerializer:

    class _HumanReadableJsonWriterVisitor(MAVisitor):

        def __init__(self):
            super().__init__()
            self._jsonWriter = MAValueJsonWriter()
            self._clear()

        def _clear(self):
            self._contexts = None
            self._processedContexts = None
            self._context = None
            #self._visitResultsStack = None
            self._visitResult = None

        #def _pushVisitResult(self):
        #    self._visitResultsStack.append(self._visitResult)
        #    self._visitResult = None

        #def _popVisitResult(self):
        #    self._visitResult = self._visitResultsStack.pop()

        def _walk(self, context):
            context_index = context.context_index
            reference_count = self._processedContexts[context_index] if context_index in self._processedContexts else 0
            self._processedContexts[context_index] = reference_count + 1
            if reference_count > 0:
                return context_index
            self._context = context
            #self._pushVisitResult()
            context.description.acceptMagritte(self)
            result = self._visitResult
            #self._popVisitResult()
            return result

        def visitElementDescription(self, aDescription):
            self._visitResult = self._jsonWriter.write_json(self._context.source, aDescription)

        def visitContainer(self, aDescription):
            result = { '_key': self._context.context_index }
            for subcontext in self._context.subcontexts:
                #subsource = subcontext.source
                subresult = self._walk(subcontext)
                result[subcontext.description.name] = subresult
            self._visitResult = result

        def visitToOneRelationDescription(self, aDescription):
            subcontext = self._context.subcontexts[0]
            self._visitResult = self._walk(subcontext)

        def visitToManyRelationDescription(self, aDescription):
            result = []
            for subcontext in self._context.subcontexts:
                #subsource = subcontext.source
                subresult = self._walk(subcontext)
                result.append(subresult)
            self._visitResult = result

        def process(self, contexts):
            self._processedContexts = {}
            self._visitResultsStack = []
            self._contexts = contexts
            result = self._walk(contexts[0]) if len(contexts) > 0 else None
            self._clear()
            return result

    def __init__(self):
        self.writerVisitor = self.__class__._HumanReadableJsonWriterVisitor()
        super().__init__()

    def dump(self, model: Any, description: MADescription) -> Any:
        descriptorWalker = MADescriptorWalker()
        contexts = descriptorWalker.dumpModel(model, description)
        result = self.writerVisitor.process(contexts)
        return result

    def serialize(self, model: Any, description: MADescription) -> str:
        dump = self.dump(model, description)
        serialized_str = json.dumps(dump)
        return serialized_str



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


if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port

    provider = TestEnvironmentProvider()
    host = provider.hosts[0]
    hostDescriptor = TestModelDescriptor.description_for("Host")
    descriptorWalker = MADescriptorWalker()
    descriptorWalker.dumpModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[0]
    portDescriptor = TestModelDescriptor.description_for("Port")
    descriptorWalker.dumpModel(port, portDescriptor)
    #testVisitor._walker._dbg_print()

    serializer = MAReferencedDataSerializer()
    serialized_str = serializer.serialize(host, hostDescriptor)
    print(serialized_str)

    #serialized_str = serializer.serialize(host, hostDescriptor.children[0])
    #print(serialized_str)


    def custom_dto_factory(description):
        if description.name == 'Host': return Host()
        if description.name == 'Port': return Port()
        return None
    deserializer = MAReferencedDataDeserializer()
    dto = deserializer.deserialize(serialized_str, hostDescriptor, dto_factory=custom_dto_factory)
    print(dto)

    serializer2 = MAReferencedDataHumanReadableSerializer()
    serialized_str2 = serializer2.serialize(host, hostDescriptor)
    print(serialized_str2)

    serialized_str2 = serializer2.serialize(port, portDescriptor)
    print(serialized_str2)