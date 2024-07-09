
from typing import Any, Iterable
import json
import re
from unicodedata import normalize
from Magritte.descriptions.MADescription_class import MADescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MAReferenceDescription_class import MAReferenceDescription
from Magritte.descriptions.MADescriptionProvider import MADescriptionProvider
from Magritte.visitors.MAVisitor_class import MAVisitor

class MADescriptionTranspiler_JS:

    class _MADescriptorTranspiler_JS_Visitor(MAVisitor):
        @staticmethod
        def variableNameByDescriptionName(description_name: str, description_names_mapping_to_js: dict) -> str:
            # Look for existing identifier
            if description_name in description_names_mapping_to_js:
                return description_names_mapping_to_js[description_name]
            # Normalize the string to form a valid Unicode identifier
            normalized_string = normalize('NFKD', description_name).encode('ascii', 'ignore').decode('ascii')
            # Replace non-alphanumeric characters and spaces with underscores
            valid_identifier = re.sub(r'\W|^(?=\d)', '_', normalized_string)
            # Remove leading and trailing underscores
            valid_identifier = valid_identifier.strip('_')
            # Add an underscore if the identifier starts with a digit
            if valid_identifier[0].isdigit():
                valid_identifier = '_' + valid_identifier
            # Add "Desc" suffix
            valid_identifier = f'{valid_identifier}Desc'
            # Check there is no already such string (because we lost some information while normalizing).
            # If yes, prepend some underscores.
            existing_identifiers = description_names_mapping_to_js.values()
            while valid_identifier in existing_identifiers:
                valid_identifier = f'_{valid_identifier}'
            # Return the valid identifier
            description_names_mapping_to_js[description_name] = valid_identifier
            return valid_identifier

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
            self._descriptionFields = None
            self._description_names_mapping_to_js = None
            self._description_classes_to_import = None
            self._transpiled_lines = None
            self._reference_description_names = None
            self._options_dict = None

        def transpile(
                self,
                anObject: MADescription,
                descriptionFields: Iterable[str],
                padding: int,
                description_names_mapping_to_js: dict,
                description_classes_to_import: set[str],
        ) -> tuple[list[str], set[str]]:
            self._descriptionFields = descriptionFields
            self._description_names_mapping_to_js = description_names_mapping_to_js
            self._description_classes_to_import = description_classes_to_import
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
            description_class_name = anObject.type
            self._description_classes_to_import.add(description_class_name)
            json_lines = self.dictToJsonLines(options_dict)
            json_lines[0] = f'new {description_class_name}({json_lines[0]}'
            json_lines[-1] = f'{json_lines[-1]})'
            self._transpiled_lines.extend(json_lines)

        def visitDescription(self, anObject: MADescription):
            super().visitDescription(anObject)
            for fieldName in self._descriptionFields:
                value = getattr(anObject, fieldName)
                self._options_dict[fieldName] = self.valueToJsonString(value)

        def visitToOneRelationDescription(self, anObject: MAReferenceDescription):
            super().visitReferenceDescription(anObject)
            reference_name = anObject.reference.name
            self._options_dict.update({
                'reference': self.variableNameByDescriptionName(reference_name, self._description_names_mapping_to_js),
            })
            self._reference_description_names.add(reference_name)

        def visitToManyRelationDescription(self, anObject: MAReferenceDescription):
            super().visitReferenceDescription(anObject)
            reference_name = anObject.reference.name
            self._options_dict.update({
                'reference': self.variableNameByDescriptionName(reference_name, self._description_names_mapping_to_js),
            })
            self._reference_description_names.add(reference_name)


    @classmethod
    def transpileDescriptionProvider(
        cls,
        descriptors: MADescriptionProvider,
        description_names_whitelist=None,
        generated_js_class_name='TranspiledDescriptors',
        magritte_js_import_prefix='magritte-js/Magritte/',
        description_field_names=(
            'name',
            'group',
            'label',
            'comment',
            'required',
            'priority',
            'visible',
            'readOnly',
            'undefinedValue',
        )
    ) -> str:
        descriptor_instantiate_lines = []
        descriptor_initialize_lines = []
        descriptor_export_lines = []
        transpiler = MADescriptionTranspiler_JS._MADescriptorTranspiler_JS_Visitor()

        # Maintain a list of descriptions that are available and which are to be transpiled
        all_descriptions = descriptors.all_descriptions
        description_names_processed = set()
        description_classes_to_import = set()
        description_names_mapping_to_js = dict()
        if description_names_whitelist is None:
            description_names_to_process = set([description.name for description in descriptors.all_descriptions])
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

                # Get unique name for variable
                js_variable_name = MADescriptionTranspiler_JS._MADescriptorTranspiler_JS_Visitor.variableNameByDescriptionName(
                    description.name, description_names_mapping_to_js
                )

                # Transpile to JS
                container_class_name = 'MAContainer'
                description_classes_to_import.add(container_class_name)
                descriptor_instantiate_lines.append(f'const {js_variable_name} = new {container_class_name}();')
                descriptor_initialize_lines.append('')
                descriptor_initialize_lines.append(f'{js_variable_name}.name = {json.dumps(container.name)};')
                descriptor_initialize_lines.append(f'{js_variable_name}.label = {json.dumps(container.label)};')
                descriptor_initialize_lines.append(f'{js_variable_name}.group = {json.dumps(container.group)};')
                descriptor_initialize_lines.append(f'{js_variable_name}.setChildren(')
                for child_description in container.children:
                    transpiled_lines, reference_description_names = transpiler.transpile(
                        child_description,
                        description_field_names,
                        4,
                        description_names_mapping_to_js,
                        description_classes_to_import,
                    )
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

        # Add description imports
        for descriptionClass in sorted(description_classes_to_import):
            js_lines.append(f"import {{ {descriptionClass} }} from '{magritte_js_import_prefix}descriptions/{descriptionClass}.js';")
        js_lines.append("")

        # Export provider class as default export
        js_lines.append(f"export default class {generated_js_class_name} {{")
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

