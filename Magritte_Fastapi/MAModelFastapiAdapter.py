
from typing import ClassVar
from inspect import signature
from Magritte.visitors.MAReferencedDataWriterReader_visitors import \
    MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer
from pydantic import JsonValue
from fastapi import Request


class MAModelFastapiAdapter:
    serializer: ClassVar = MAReferencedDataHumanReadableSerializer()
    deserializer: ClassVar = MAReferencedDataHumanReadableDeserializer()

    @staticmethod
    def describe(request_descriptor=None, response_descriptor=None, dto_factory=None):
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

            async def wrapper_decorator_without_argument() -> JsonValue:
                response = await callback()
                return send_response(response)

            async def wrapper_decorator_with_path_argument(request_body: Request) -> JsonValue:
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

            if callback_has_parameters:
                if request_descriptor is None:
                    return wrapper_decorator_with_path_argument
                else:
                    return wrapper_decorator_with_request_argument
            else:
                return wrapper_decorator_without_argument

        return describe_decorator



if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port
    from fastapi import FastAPI
    import uvicorn


    provider = TestEnvironmentProvider()
    host = provider.hosts[0]
    hostDescriptor = TestModelDescriptor.description_for("Host")
    #descriptorWalker = MADescriptorWalker()
    #descriptorWalker.dumpModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[5]
    portDescriptor = TestModelDescriptor.description_for("Port")


    app = FastAPI()


    @app.get("/")
    @MAModelFastapiAdapter.describe(response_descriptor=hostDescriptor)
    async def index():
        response = host
        return response

    @app.post("/test")
    @MAModelFastapiAdapter.describe(request_descriptor=hostDescriptor, response_descriptor=portDescriptor)
    async def test(request: Host) -> Port:
        return request.ports[2]

    uvicorn.run(app, host="0.0.0.0", port=8000)
