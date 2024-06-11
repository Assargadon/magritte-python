
from fastapi import FastAPI
from MAModelFastapiAdapter import MAModelFastapiAdapter
from Magritte.descriptions.MAToManyRelationDescription_class import MAToManyRelationDescription
from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.accessors.MAIdentityAccessor_class import MAIdentityAccessor


if __name__ == "__main__":

    from Magritte.model_for_tests.EnvironmentProvider_test import TestEnvironmentProvider
    from Magritte.model_for_tests.ModelDescriptor_test import TestModelDescriptor, Host, User, Account
    import uvicorn


    provider = TestEnvironmentProvider()
    hostDescriptor = TestModelDescriptor.description_for("Host")
    accountDescriptor = TestModelDescriptor.description_for("Account")
    userDescriptor = TestModelDescriptor.description_for("User")

    app = FastAPI()


# ============= EXAMPLE ====================

    @app.get("/host/{host_index}")
    @MAModelFastapiAdapter.describe(response_descriptor=hostDescriptor)
    async def get_host(host_index):
        host_id_int = int(host_index)
        return provider.hosts[host_id_int]

    @app.get("/account/{account_index}")
    @MAModelFastapiAdapter.describe(response_descriptor=accountDescriptor)
    async def get_account(account_index):
        account_id_int = int(account_index)
        return provider.accounts[account_id_int]

    @app.get("/user/{user_index}")
    @MAModelFastapiAdapter.describe(response_descriptor=userDescriptor)
    async def get_user(user_index):
        user_id_int = int(user_index)
        return provider.users[user_id_int]

    @app.post("/test_user")
    @MAModelFastapiAdapter.describe(request_descriptor=userDescriptor)
    async def post_user(user: User):
        user1 = provider.users[1]
        s = f'User date of birth: {user.dateofbirth} // User 1 date of birth: {user1.dateofbirth}'
        print(s)
        return s

    @app.post("/test_account")
    @MAModelFastapiAdapter.describe(request_descriptor=accountDescriptor)
    async def post_account(account: Account):
        account1 = provider.accounts[1]
        s = f'Account registration timestamp: {account.reg_timestamp} // Account 1 timestamp: {account1.reg_timestamp}'
        print(s)
        return s

    @app.get("/hosts")
    @MAModelFastapiAdapter.describe(response_descriptor=MAToManyRelationDescription(reference=hostDescriptor, accessor=MAIdentityAccessor()))
    async def get_hosts():
        return provider.hosts

    @app.post("/hosts_list")
    @MAModelFastapiAdapter.describe(request_descriptor=MAToManyRelationDescription(reference=hostDescriptor)) # not working (todo if needed)
    async def post_hosts(hosts):
        print(hosts)
        return "OK"

    @app.post("/add_host")
    @MAModelFastapiAdapter.describe(request_descriptor=hostDescriptor, response_descriptor=MAStringDescription(accessor=MAIdentityAccessor()))
    async def add_host(host):
        provider.hosts.append(host)
        return "OK"

    @app.get("/desc/host")
    @MAModelFastapiAdapter.describe(response_descriptor=hostDescriptor.magritteDescription())
    async def host_desc():
        return hostDescriptor


    test_get_params_descriptor = MAContainer()
    test_get_params_descriptor.setChildren(
        [
            MAIntDescription(
                name='int_val', label='int', required=True
            ),
            MAStringDescription(
                name='str_val', label='str', required=False
            ),
        ]
    )

    @app.get("/test_described_search_query_params")
    @MAModelFastapiAdapter.describe(search_query_descriptor=test_get_params_descriptor, response_descriptor=MAStringDescription())
    async def test_described_search_query_params(params_dict):
        return f"OK: {str(params_dict)}"



# ============= /EXAMPLE ====================


    uvicorn.run(app, host="0.0.0.0", port=8000)
