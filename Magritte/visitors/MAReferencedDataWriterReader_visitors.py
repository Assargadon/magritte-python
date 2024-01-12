
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
            source: Any = None
            description: MADescription = None
            #value_index: int = None
            subcontexts: list = None
            _dbg_ref_count: int = 1
            #_dbg_value: None

        def __init__(self):
            self._contexts = None
            self._contexts_by_source_id = None
            self._values = None
            self._values_by_value_index = None
            self._value_indices_by_identifier = None
            self._value_indices_by_context_index = None
            self._clear()

        def _clear(self):
            self._contexts = []
            self._contexts_by_source_id = {}
            self._values = []
            self._values_by_value_index = {}
            self._value_indices_by_identifier = {}
            self._value_indices_by_context_index = {}

        def _createEmptyContext(self):
            context_index = len(self._contexts)
            self._context = self.__class__._Context()
            self._contexts.append(self._context)
            self._context.context_index = context_index
            return self._context

        def _addValue(self, aValue):
            value_index = len(self._values)
            self._values.append(aValue)
            self._values_by_value_index[value_index] = aValue
            return value_index

        def _addValueWithCheck(self, aValue):
            identifier = id(aValue)
            if identifier in self._value_indices_by_identifier:
                was_added = False
                value_index = self._value_indices_by_identifier[identifier]
            else:
                was_added = True
                value_index = len(self._values)
                self._values.append(aValue)
                self._value_indices_by_identifier[identifier] = value_index
                self._values_by_value_index[value_index] = aValue
            return (value_index, was_added,)

        def _walkFromCurrent(self):
            description = self._context.description
            model = self._context.source
            if model == description.undefinedValue:
                return
            if not description.visible:
                return
            description.acceptMagritte(self)

        def visitElementDescription(self, description: MADescription):
            context = self._context
            value = self.processElementDescriptionContext(context)
            value_index = self._addValue(value)
            self._value_indices_by_context_index[context.context_index] = value_index

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
            value, subsource = self.processToOneRelationContext(context, description)
            (value_index, was_added,) = self._addValueWithCheck(value)
            if was_added:
                subcontext = self._createEmptyContext()
                subcontext.source = subsource
                subcontext.description = description.reference
                self._contexts_by_source_id[value_index] = subcontext
                self._walkFromCurrent()
            else:
                subcontext = self._contexts_by_source_id[value_index]
                subcontext._dbg_ref_count += 1
            context.subcontexts = [subcontext]

        def visitToManyRelationDescription(self, description):
            context = self._context
            manyRelations = self.processToManyRelationContext(context, description)
            context.subcontexts = []
            for relation in manyRelations:
                (value, subsource,) = relation
                (value_index, was_added,) = self._addValueWithCheck(value)
                if was_added:
                    subcontext = self._createEmptyContext()
                    subcontext.source = subsource
                    subcontext.description = description.reference
                    self._contexts_by_source_id[value_index] = subcontext
                    self._walkFromCurrent()
                else:
                    subcontext = self._contexts_by_source_id[value_index]
                    subcontext._dbg_ref_count += 1
                context.subcontexts.append(subcontext)

        def processRootContext(self, context):
            return None

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
            value = self.processRootContext(self._context)
            (value_index, was_added,) = self._addValueWithCheck(value)
            self._contexts_by_source_id[value_index] = self._context
            self._walkFromCurrent()
            return self._contexts


    class _ModelDumpWalkerVisitor(_WalkerVisitor):
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
                    print(f'{subPrefix}Value of {aContext.description.name}, {self._values[self._value_indices_by_context_index[aContext.context_index]]}')
                else:
                    for subcontext in aContext.subcontexts:
                        subcontext_index = subcontext.context_index
                        if subcontext_index in printed_contexts:
                            print(f'{subPrefix}Context {subcontext_index}, {subcontext.description.name} // already printed')
                        else:
                            printContext(subPrefix, subcontext)

            printContext('', self._contexts[0])

        def processRootContext(self, context):
            value = context.source
            return value

        def processElementDescriptionContext(self, context):
            if self._doReadElementValues:
                value = MAModel.readUsingWrapper(context.source, context.description)
                return value
            else:
                return None

        def processToOneRelationContext(self, context, description):
            model = context.source
            value = MAModel.readUsingWrapper(model, description)
            return (value, value,)

        def processToManyRelationContext(self, context, description):
            values = MAModel.readUsingWrapper(context.source, description)
            manyRelations = [(value, value,) for value in values]
            return manyRelations

        def processModel(self, aModel: Any, aDescription: MADescription, doReadElementValues=False):
            self._doReadElementValues = doReadElementValues
            return super().walkDescription(aModel, aDescription)


    def processModel(self, aModel: Any, aDescription: MADescription):
        walker = self.__class__._ModelDumpWalkerVisitor()
        return walker.processModel(aModel, aDescription)


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
        contexts = descriptorWalker.processModel(model, description)
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
    testVisitor = MADescriptorWalker()
    testVisitor.processModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[0]
    portDescriptor = TestModelDescriptor.description_for("Port")
    testVisitor.processModel(port, portDescriptor)
    #testVisitor._walker._dbg_print()

    jsonWriter = MAReferencedDataJsonWriter()
    j = jsonWriter.write_json(host, hostDescriptor)
    print(j)

    jsonReader = MAReferencedDataJsonReader()
    dto = jsonReader.read_json(j, hostDescriptor)
    print(dto)
