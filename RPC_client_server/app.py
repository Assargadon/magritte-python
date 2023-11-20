import uvicorn
import asyncio

from fastapi import APIRouter, FastAPI, WebSocket
from fastapi import FastAPI
from fastapi_websocket_rpc.utils import gen_uid
from fastapi_websocket_rpc.websocket_rpc_endpoint import WebsocketRPCEndpoint
from RPC_client_server.rpc_handler import MAWebSocketRpcBase


class MAServer(MAWebSocketRpcBase):
    '''Some custom methods to realize'''
    """
    async def gen_user_status(self, person_json: str) -> Any:
        #asyncio.create_task(self.channel.other.allow_exit())
        log.debug('HERE')
        person_obj = await _deserialize_params(json_obj=person_json, desc=ma_req_desc)

        response_obj = ResponseObject()

        setattr(response_obj, 'active', person_obj.active)
        setattr(response_obj, 'period_active', person_obj.period_active)
        setattr(response_obj, 'name', person_obj.name)
        setattr(response_obj, 'processing_timestamp', datetime.now())

        resp_json = await _serialize_response(obj=response_obj, desc=ma_req_desc)

        return resp_json
    """
    pass

# Configurable
PORT = "8080"
CLIENT_ID = gen_uid()
uri = f"ws://localhost:{PORT}/ws/{CLIENT_ID}"


async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())


"""Initialize server with FastAPI app and router"""
app = FastAPI()
router = APIRouter()
endpoint = WebsocketRPCEndpoint(MAServer(), on_connect=[on_connect])

@router.websocket("/ws/{client_id}")
async def websocket_rpc_endpoint(websocket: WebSocket, client_id: str):
    await endpoint.main_loop(websocket, client_id)

endpoint.register_route(app)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, port=PORT)