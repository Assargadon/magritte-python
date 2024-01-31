
from typing import ClassVar
from Magritte.visitors.MAReferencedDataWriterReader_visitors import \
    MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer
from fastapi import FastAPI
from pydantic import JsonValue
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor

class MAModelFastapiAdapter:
    serializer: ClassVar = MAReferencedDataHumanReadableSerializer()
    deserializer: ClassVar = MAReferencedDataHumanReadableDeserializer()

    @staticmethod
    def describe(request_descriptor, response_descriptor, dto_factory=None):
        if dto_factory is None:
            dto_factory = MAReferencedDataHumanReadableDeserializer.default_dto_factory

        def describe_decorator(callback):

            async def wrapper_decorator_without_argument() -> JsonValue:
                response = await callback()
                response_dump = MAModelFastapiAdapter.serializer.dumpHumanReadable(
                    response,
                    response_descriptor
                )
                return response_dump

            async def wrapper_decorator_with_argument(request_dump: dict) -> JsonValue:
                request = MAModelFastapiAdapter.deserializer.instaniateHumanReadable(
                    request_dump,
                    request_descriptor,
                    dto_factory=dto_factory
                )
                response = await callback(request)
                response_dump = MAModelFastapiAdapter.serializer.dumpHumanReadable(
                    response,
                    response_descriptor
                )
                return response_dump

            return wrapper_decorator_without_argument if request_descriptor is None else wrapper_decorator_with_argument

        return describe_decorator



if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, Port
    import uvicorn


    provider = TestEnvironmentProvider()
    host = provider.hosts[0]
    hostDescriptor = TestModelDescriptor.description_for("Host")
    #descriptorWalker = MADescriptorWalker()
    #descriptorWalker.dumpModel(host, hostDescriptor)
    #testVisitor._walker._dbg_print()

    port = host.ports[5]
    portDescriptor = TestModelDescriptor.description_for("Port")

    def custom_dto_factory(description):
        if description.name == 'Host': return Host()
        if description.name == 'Port': return Port()
        return None


    app = FastAPI()



    @app.get("/")
    @MAModelFastapiAdapter.describe(request_descriptor=None, response_descriptor=hostDescriptor)
    async def index():
        response = host
        return response

    @app.post("/test")
    @MAModelFastapiAdapter.describe(request_descriptor=hostDescriptor, response_descriptor=portDescriptor)
    async def test(request: Host) -> Port:
        return request.ports[2]

# ============= EXAMPLE ====================
    @app.get("/hosts")
    @MAModelFastapiAdapter.describe(request_descriptor=None, response_descriptor=MAToManyRelationDescription(reference=hostDescriptor, accessor=MAIdentityAccessor()))
    async def get_hosts():
        return provider.hosts

    @app.post("/add_host")
    @MAModelFastapiAdapter.describe(request_descriptor=hostDescriptor, response_descriptor=MAStringDescription(accessor=MAIdentityAccessor()))
    async def add_host(host):
        provider.hosts.append(host)
        return "OK"

    @app.get("/desc/host")
    @MAModelFastapiAdapter.describe(request_descriptor=None, response_descriptor=hostDescriptor.magritteDescription())
    async def host_desc():
        return hostDescriptor

# ============= /EXAMPLE ====================


    uvicorn.run(app, host="0.0.0.0", port=8000)
