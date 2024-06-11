
from copy import copy
from typing import ClassVar
from inspect import signature
from Magritte.visitors.MAReferencedDataWriterReader_visitors import \
    MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer
from Magritte.accessors.MAAttrAccessor_class import MAAttrAccessor
from pydantic import JsonValue, BaseModel, create_model
from fastapi import Request, Depends


class MAModelFastapiAdapter:
    serializer: ClassVar = MAReferencedDataHumanReadableSerializer()
    deserializer: ClassVar = MAReferencedDataHumanReadableDeserializer()

    @staticmethod
    def describe(search_query_descriptor=None, request_descriptor=None, response_descriptor=None, dto_factory=None):
        if dto_factory is None:
            dto_factory = MAReferencedDataHumanReadableDeserializer.default_dto_factory

        def describe_decorator(callback):

            def send_response(response):
                if response_descriptor is None:
                    return response
                else:
                    response_dump = MAModelFastapiAdapter.serializer.dumpHumanReadable(
                        response,
                        response_descriptor
                    )
                    return response_dump

            sig = signature(callback)
            callback_parameters = sig.parameters
            callback_has_parameters = len(callback_parameters) > 0

            decorator_with_request_argument = False
            decorator_with_search_query_encoded_argument = False
            decorator_with_named_path_arguments = False
            decorator_without_argument = False
            if callback_has_parameters:
                if request_descriptor is not None:
                    decorator_with_request_argument = True
                elif search_query_descriptor is not None:
                    decorator_with_search_query_encoded_argument = True
                else:
                    decorator_with_named_path_arguments = True
            else:
                decorator_without_argument = True

            if decorator_with_search_query_encoded_argument:
                search_query_params = dict()
                for description in search_query_descriptor.children:
                    param_name = description.name
                    if description.isRequired():
                        search_query_params[param_name] = (str, ...)
                    else:
                        search_query_params[param_name] = (str | None, None)
                SearchQueryParams = create_model("SearchQueryParams", **search_query_params)
            else:
                SearchQueryParams = None

            async def wrapper_decorator_without_argument() -> JsonValue:
                response = await callback()
                return send_response(response)

            async def wrapper_decorator_with_named_path_arguments(request_body: Request) -> JsonValue:
                args = []
                path_params = request_body.path_params
                for param_name in callback_parameters:
                    if param_name in path_params:
                        args.append(path_params[param_name])
                    else:
                        args.append(None)
                response = await callback(*args)
                return send_response(response)

            async def wrapper_decorator_with_request_argument(request_body: Request) -> JsonValue:
                request_dump = await request_body.json()
                request = MAModelFastapiAdapter.deserializer.instantiateHumanReadable(
                    request_dump,
                    request_descriptor,
                    dto_factory=dto_factory
                )
                response = await callback(request)
                return send_response(response)

            class SearchQueryParams_(BaseModel):
                #body: Optional[str] = ""
                str_val: str = "A"
                int_val: str = "1"

            async def wrapper_decorator_with_search_query_encoded_argument(query_params: SearchQueryParams = Depends()) -> JsonValue:
                request = dict()
                for description in search_query_descriptor.children:
                    param_name = description.name
                    value_str = getattr(query_params, param_name)

                    if value_str is not None:
                        description_clone = copy(description)
                        description_clone.accessor = MAAttrAccessor(param_name)
                        value = description_clone.readString(query_params)
                    elif not description.isRequired():
                        value = description.default
                    else:
                        raise ValueError(f'The GET request is missing required argument {param_name}')
                    request[param_name] = value
                response = await callback(request)
                return send_response(response)

            if decorator_with_request_argument:
                return wrapper_decorator_with_request_argument
            if decorator_with_search_query_encoded_argument:
                return wrapper_decorator_with_search_query_encoded_argument
            if decorator_with_named_path_arguments:
                return wrapper_decorator_with_named_path_arguments
            if decorator_without_argument:
                return wrapper_decorator_without_argument

        return describe_decorator

