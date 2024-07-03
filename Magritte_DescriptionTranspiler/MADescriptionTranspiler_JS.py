
from typing import Any
import json
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MADescriptionProvider import MADescriptionProvider
from Magritte.visitors.MAVisitor_class import MAVisitor

class MADescriptionTranspiler_JS:

    class _MADescriptorTranspiler_JS_Visitor(MAVisitor):
        @staticmethod
        def variableNameByDescriptionName(description_name: str) -> str:
            return f'{description_name.lower()}Desc'

        @staticmethod
        def valueToJsonString(value: Any) -> str:
            if value is None:
                return 'undefined'
            else:
                return json.dumps(value)

        @staticmethod
        def dictToJsonLines(d: dict) -> list[str]:
            json_lines = ['{']
            for key, value in d.items():
                json_lines.append(f'    {key}: {value},')
            json_lines.append('}')
            return json_lines

        def __init__(self):
            self._transpiled_lines = None
            self._reference_description_names = None
            self._options_dict = None

        def transpile(self, anObject: MADescription, padding: int) -> tuple[list[str], set[str]]:
            self._transpiled_lines = []
            self._reference_description_names = set()
            self._options_dict = {}
            self.visit(anObject)
            self._createDescriptionWithOptions(anObject, self._options_dict)
            pad_str = ' '*padding
            for i in range(len(self._transpiled_lines)):
                self._transpiled_lines[i] = f'{pad_str}{self._transpiled_lines[i]}'
            return self._transpiled_lines, self._reference_description_names

        def _createDescriptionWithOptions(self, anObject, options_dict):
            json_lines = self.dictToJsonLines(options_dict)
            json_lines[0] = f'new {anObject.type}({json_lines[0]}'
            json_lines[-1] = f'{json_lines[-1]})'
            self._transpiled_lines.extend(json_lines)

        def visitDescription(self, anObject: MADescription):
            super().visitDescription(anObject)
            self._options_dict.update({
                'name': self.valueToJsonString(anObject.name),
                'group': self.valueToJsonString(anObject.group),
                'label': self.valueToJsonString(anObject.label),
                'required': self.valueToJsonString(anObject.required),
                'priority': self.valueToJsonString(anObject.priority),
                'visible': self.valueToJsonString(anObject.visible),
            })

        def visitToOneRelationDescription(self, anObject: MAReferenceDescription):
            super().visitReferenceDescription(anObject)
            reference_name = anObject.reference.name
            self._options_dict.update({
                'reference': self.variableNameByDescriptionName(reference_name),
            })
            self._reference_description_names.add(reference_name)

        def visitToManyRelationDescription(self, anObject: MAReferenceDescription):
            super().visitReferenceDescription(anObject)
            reference_name = anObject.reference.name
            self._options_dict.update({
                'reference': self.variableNameByDescriptionName(reference_name),
            })
            self._reference_description_names.add(reference_name)


    @classmethod
    def transpileDescriptionProvider(
        cls,
        descriptors: MADescriptionProvider,
        description_names_whitelist=None,
        generated_js_class_name='TranspiledDescriptors',
        magritte_js_import_prefix='magritte-js/Magritte/',
    ) -> str:
        descriptor_instantiate_lines = []
        descriptor_initialize_lines = []
        descriptor_export_lines = []
        transpiler = MADescriptionTranspiler_JS._MADescriptorTranspiler_JS_Visitor()

        # Maintain a list of descriptions that are available and which are to be transpiled
        all_descriptions = descriptors.all_descriptions
        description_names_processed = set()
        if description_names_whitelist is None:
            description_names_to_process = set([description.name for description in descriptors.descriptions()])
        else:
            description_names_to_process = set(description_names_whitelist)

        # Walk the descriptions
        while len(description_names_to_process) > 0:
            new_description_names_to_process = set()
            for description_name in description_names_to_process:

                # Do not process it again
                if description_name in description_names_processed:
                    continue

                # Find the description in provider
                description = next((description for description in all_descriptions if description.name == description_name), None)
                if description is None:
                    raise TypeError(f'The required description {description_name} is not provided by MADescriptionProvider')

                # Check if it is MAContainer
                if isinstance(description, MAContainer):
                    container: MAContainer = description
                else:
                    raise TypeError(f'{cls.__name__} can transpile only MAContainer descriptions')

                # Transpile to JS
                js_variable_name = MADescriptionTranspiler_JS._MADescriptorTranspiler_JS_Visitor.variableNameByDescriptionName(description.name)
                descriptor_instantiate_lines.append(f'const {js_variable_name} = new MAContainer();')
                descriptor_initialize_lines.append('')
                descriptor_initialize_lines.append(f'{js_variable_name}.name = {json.dumps(container.name)};')
                descriptor_initialize_lines.append(f'{js_variable_name}.label = {json.dumps(container.label)};')
                descriptor_initialize_lines.append(f'{js_variable_name}.setChildren(')
                for child_description in container.children:
                    transpiled_lines, reference_description_names = transpiler.transpile(child_description, 4)
                    transpiled_lines[-1] = f'{transpiled_lines[-1]},'
                    descriptor_initialize_lines.extend(transpiled_lines)
                    new_description_names_to_process.update(reference_description_names)
                descriptor_initialize_lines.append(f');')

                descriptor_export_lines.append(f'this.descriptions_by_model_type.set({json.dumps(container.name)}, {js_variable_name});')
                descriptor_export_lines.append(f'this.all_descriptions.push({js_variable_name});')

                # Save in processed list
                description_names_processed.add(description_name)

            description_names_to_process = new_description_names_to_process

        # Add a padding in the method
        pad_str = ' '*8
        for i in range(len(descriptor_instantiate_lines)):
            descriptor_instantiate_lines[i] = f'{pad_str}{descriptor_instantiate_lines[i]}'
        for i in range(len(descriptor_initialize_lines)):
            descriptor_initialize_lines[i] = f'{pad_str}{descriptor_initialize_lines[i]}'
        for i in range(len(descriptor_export_lines)):
            descriptor_export_lines[i] = f'{pad_str}{descriptor_export_lines[i]}'

        # Add header
        js_lines = []
        js_lines.append(f"import {{ MAContainer }} from '{magritte_js_import_prefix}descriptions/MAContainer.js';")
        js_lines.append(f"import {{ MAToOneRelationDescription }} from '{magritte_js_import_prefix}descriptions/MAToOneRelationDescription.js';")
        js_lines.append(f"import {{ MAToManyRelationDescription }} from '{magritte_js_import_prefix}descriptions/MAToManyRelationDescription.js';")
        js_lines.append(f"import {{ MAStringDescription }} from '{magritte_js_import_prefix}descriptions/MAStringDescription.js';")
        js_lines.append(f"import {{ MAIntDescription }} from '{magritte_js_import_prefix}descriptions/MAIntDescription.js';")
        js_lines.append(f"import {{ MAElementDescription }} from '{magritte_js_import_prefix}descriptions/MAElementDescription.js';")
        js_lines.append(f"import {{ MABooleanDescription }} from '{magritte_js_import_prefix}descriptions/MABooleanDescription.js';")
        js_lines.append(f"import {{ MAPriorityContainer }} from '{magritte_js_import_prefix}descriptions/MAPriorityContainer.js';")
        js_lines.append("")
        js_lines.append(f"class {generated_js_class_name} {{")
        js_lines.append("    constructor () {")
        js_lines.append("        this.descriptions_by_model_type = new Map();")
        js_lines.append("        this.all_descriptions = [];")

        # Add generated code
        js_lines.extend(descriptor_instantiate_lines)
        js_lines.extend(descriptor_initialize_lines)
        js_lines.extend(descriptor_export_lines)

        # Add footer
        js_lines.append("    }")
        js_lines.append("}")
        js_lines.append("")

        # Put it all together
        return '\n'.join(js_lines)


if __name__ == "__main__":

    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptorProvider
    descriptors = TestModelDescriptorProvider()
    t = MADescriptionTranspiler_JS()
    s = t.transpileDescriptionProvider(
        descriptors,
        description_names_whitelist=['Host'],
        generated_js_class_name=type(descriptors).__name__,
        magritte_js_import_prefix='./Magritte/'
    )
    print(s)
    with open("output.mjs", "w") as js_file:
        js_file.write(s)

