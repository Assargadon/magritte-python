
from typing import Any, Union
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.visitors.MAVisitor_class import MAVisitor
from Magritte.MAModel_class import MAModel
from Magritte.visitors.MAJsonWriter_visitors import MAValueJsonWriter


class MADescriptorWalker:

    class _WalkerVisitor(MAVisitor):

        class _Context:
            context_index: int = None
            source: Any = None                          # Arbitrary object reference related to the context. Used to get targets from somewhere to break cyclic references and extract subsources for subcontexts.
            description: MADescription = None
            subcontexts: list = None
            _dbg_ref_count: int = 1

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

        def _addSourceWithCheck(self, source):
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
            source = self.processElementDescriptionContext(context)
            source_index = self._addSource(source)
            self._source_indices_by_context_index[context.context_index] = source_index

        def visitContainer(self, description: MAContainer):
            context = self._context
            context.subcontexts = []
            for subdescription in description:
                subcontext = self._createEmptyContext()
                context.subcontexts.append(subcontext)
                subcontext.source = context.source
                subcontext.description = subdescription
                self._walkFromCurrent()

        def visitToOneRelationDescription(self, description: MAReferenceDescription):
            context = self._context
            subsource = self.processToOneRelationContext(context, description)
            (subsource_index, was_added,) = self._addSourceWithCheck(subsource)
            if was_added:
                subcontext = self._createEmptyContext()
                subcontext.source = subsource
                subcontext.description = description.reference
                self._contexts_by_source_id[subsource_index] = subcontext
                self._walkFromCurrent()
            else:
                subcontext = self._contexts_by_source_id[subsource_index]
                subcontext._dbg_ref_count += 1
            context.subcontexts = [subcontext]

        def visitToManyRelationDescription(self, description):
            context = self._context
            subsources = self.processToManyRelationContext(context, description)
            context.subcontexts = []
            for subsource in subsources:
                (subsource_index, was_added,) = self._addSourceWithCheck(subsource)
                if was_added:
                    subcontext = self._createEmptyContext()
                    subcontext.source = subsource
                    subcontext.description = description.reference
                    self._contexts_by_source_id[subsource_index] = subcontext
                    self._walkFromCurrent()
                else:
                    subcontext = self._contexts_by_source_id[subsource_index]
                    subcontext._dbg_ref_count += 1
                context.subcontexts.append(subcontext)

        def processElementDescriptionContext(self, context):
            return None

        def processToOneRelationContext(self, context, description):
            return (None, None,)

        def processToManyRelationContext(self, context, description):
            return []

        def walkDescription(self, aSource: Any, aDescription: MADescription):
            self._clear()
            self._createEmptyContext()
            self._context.source = aSource
            self._context.description = aDescription
            (source_index, was_added,) = self._addSourceWithCheck(aSource)
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
                print(f'{sPrefix}Context {context_index}, {aContext.description.name}, referenced {aContext._dbg_ref_count} time(s):')
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

        def processElementDescriptionContext(self, context):
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

        def processModel(self, aModel: Any, aDescription: MADescription, doReadElementValues):
            self._doReadElementValues = doReadElementValues
            return super().walkDescription(aModel, aDescription)


    def dumpModel(self, aModel: Any, aDescription: MADescription, doReadElementValues=False):
        walker = self.__class__._DumpModelWalkerVisitor()
        return walker.processModel(aModel, aDescription, doReadElementValues)


class MAReferencedDataJsonWriter:

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
        if context.context_index in contexts:
            return
        result = { 'name': context.description.name }
        contexts[context.context_index] = result

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
                subcontext_indices.append(subcontext.context_index)
                self._walkFromCurrent(contexts, subcontext)
            result['subcontext_indices'] = subcontext_indices

    def write_json(self, model, description):
        descriptorWalker = MADescriptorWalker()
        contexts = descriptorWalker.dumpModel(model, description)
        result = { 'contexts': {}, 'root_context_index': None }
        if len(contexts) > 0:
            result['root_context_index'] = 0
            self._walkFromCurrent(result['contexts'], contexts[0])
        return result


class MAReferencedDataJsonReader:

    @classmethod
    def default_dto_factory(cls, description):
        c = description.kind
        return c()

    def read_json(self, json, description, dto_factory=default_dto_factory):
        pass



if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor

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

    jsonWriter = MAReferencedDataJsonWriter()
    j = jsonWriter.write_json(host, hostDescriptor)
    print(j)

    jsonReader = MAReferencedDataJsonReader()
    dto = jsonReader.read_json(j, hostDescriptor)
    print(dto)
