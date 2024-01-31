
from fastapi import FastAPI
from MAModelFastapiAdapter import MAModelFastapiAdapter
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor


if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host
    import uvicorn


    provider = TestEnvironmentProvider()
    hostDescriptor = TestModelDescriptor.description_for("Host")


    app = FastAPI()


# ============= EXAMPLE ====================

    @app.get("/host/{host_index}")
    @MAModelFastapiAdapter.describe(request_descriptor=None, response_descriptor=hostDescriptor)
    async def get_host(host_index):
        host_id_int = int(host_index)
        return provider.hosts[host_id_int]

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
