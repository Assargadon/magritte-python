import logging
import json
import sys

import asyncio
from multiprocessing import Process
import uvicorn
import unittest

from fastapi import APIRouter, FastAPI, WebSocket
from fastapi_websocket_rpc.websocket_rpc_endpoint import WebsocketRPCEndpoint
from fastapi_websocket_rpc import WebSocketRpcClient
from fastapi_websocket_rpc.utils import gen_uid
from RPC_client_server.rpc_handler import MAWebSocketRpcBase
from datetime import datetime, timedelta, date, time

from RPC_client_server.client import MAWaitingClient

from Magritte.descriptions.MAStringDescription_class import MAStringDescription
from Magritte.descriptions.MADateDescription_class import MADateDescription
from Magritte.descriptions.MATimeDescription_class import MATimeDescription
from Magritte.descriptions.MAIntDescription_class import MAIntDescription
from Magritte.descriptions.MABooleanDescription_class import MABooleanDescription
from Magritte.descriptions.MAFloatDescription_class import MAFloatDescription
from Magritte.descriptions.MADurationDescription_class import MADurationDescription
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from Magritte.descriptions.MAContainer_class import MAContainer

from Magritte.visitors.MAJsonWriterReader_visitors import ResponseObject


#Debugging
DEBUGMODE=True
logging.basicConfig(level=logging.DEBUG)
log=logging.getLogger('=>')  
sys.stdout = open('output.txt', 'w')


ma_req_desc = MAContainer()
ma_req_desc.label = "Test Request description"
ma_req_desc.setChildren(
    [
        MAStringDescription(
            name='first_name', 
            label='First name', 
            accessor='first_name'
        ),
        MADateDescription(
            name='dob', 
            label='Birth date', 
            default=date(1990, 1, 1),
            accessor='dob'
        ),
        MADateAndTimeDescription(
            name='last_active',
            label='Last time active',
            default=datetime(2023, 10, 30, 10, 10, 10),
            accessor='last_active'
        ),
        MATimeDescription(
            name='current_time',
            label='Current time',
            default=time(18, 4, 12),
            accessor='current_time'
        ),
        MAIntDescription(
            name='height', 
            label='height', 
            default=180,
            accessor='height'
        ),
        MAFloatDescription(
            name='age', 
            label='age', 
            default=33.5, 
            accessor='age'
        ),
        MABooleanDescription(
            name='alive', 
            label='alive', 
            default=True,
            accessor='alive'
        ),
        MABooleanDescription(
            name='active', 
            label='active', 
            default=False,
            accessor='active'
        ),
        MADurationDescription(
            name='period_active', 
            label='period_active', 
            default=datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1),
            accessor='period_active'
        )
    ]
)
ma_resp_desc = MAContainer()
ma_resp_desc.label = "Test Response description"
ma_resp_desc.setChildren(
    [
        MAStringDescription(
            name='first_name', 
            label='First name',
            accessor='first_name'
        ),
        MABooleanDescription(
            name='active', 
            label='active', 
            accessor='active'
        ),
        MADurationDescription(
            name='period_active', 
            label='period_active',
            accessor='period_active',
        ),
        MADateAndTimeDescription(
            name='processing_timestamp',
            label='Processing timestamp',
            accessor='processing_timestamp',
        )
    ]
)


class TestServer(MAWebSocketRpcBase):
    '''
    async def gen_user_status(self, person_json: str) -> Any:
        #asyncio.create_task(self.channel.other.allow_exit())
        log.debug('GEN_USER_STATUS_1')
        person_obj = await _deserialize_params(json_obj=person_json, desc=ma_req_desc)

        log.debug('GEN_USER_STATUS_2: _deserealize params OK')
        log.debug(f"PERSON OBJ: {person_obj}")
        response_obj = ResponseObject()

        setattr(response_obj, 'active', person_obj.active)
        setattr(response_obj, 'period_active', person_obj.period_active)
        setattr(response_obj, 'name', person_obj.name)
        setattr(response_obj, 'processing_timestamp', datetime.now())

        log.debug('GEN_USER_STATUS_3: respobse object OK')
        log.debug(f"RESP OBJ: {response_obj}")

        resp_json = await _serialize_response(obj=response_obj, desc=ma_req_desc)

        log.debug('GEN_USER_STATUS_4: resp_json OK')
        log.debug(f"RESP JSON: {resp_json}")
        return resp_json
    '''

    async def concat(self, a="", b=""):
        return a + b
    
    async def call_client_handlers(self):
        # allow client to exit after some time after
        asyncio.create_task(self.channel.other.allow_exit(delay=4))
        client_handlers = await self.channel.other.gen_self_handlers()

        return client_handlers.result


# Configurable
PORT = "8080"
CLIENT_ID = gen_uid()
uri = f"ws://localhost:{PORT}/ws/{CLIENT_ID}"

async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())

def setup_server():
    app = FastAPI()
    router = APIRouter()

    endpoint = WebsocketRPCEndpoint(TestServer(), on_connect=[on_connect])

    @router.websocket("/ws/{client_id}")
    async def websocket_rpc_endpoint(websocket: WebSocket, client_id: str):
        await endpoint.main_loop(websocket, client_id)

    endpoint.register_route(app)
    app.include_router(router)
    uvicorn.run(app, port=PORT)

    assert endpoint.server


"""
Tests models and Descs for future serialize and deserialize
"""
json_req_desq = json.dumps({
        "first_name": "Paul",
        "dob": str(date(1990, 11, 14)), 
        "height": 180, 
        "age": 33.5,
        "alive": True,
        "active": False,
        "period_active": str(datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1)),
        "last_active": str(datetime(2023, 10, 30, 10, 10, 10)),
        "current_time": str(time(18, 4, 12))
    }
)

json_resp_desq = json.dumps({
        "name": "Paul",
        "active": False,
        "period_active": str(datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1)),
        "processing_timestamp": str(datetime.now())
    }
)

"""Obj model for future tests"""

class TestPerson():
    def __init__(
            self, 
            first_name, 
            age, 
            dob, 
            height, 
            alive, 
            active, 
            last_acitve,
            period_active,
            current_time
    ):
        self.first_name = first_name
        self.dob = dob
        self.age = age
        self.height = height
        self.alive = alive
        self.active = active,
        self.last_active = last_acitve
        self.period_active = period_active
        self.current_time = current_time


class TestRPCMethods(unittest.TestCase):
    def setUp(self):
        self.handler_name = 'person_handler'

        self.model = TestPerson(
            first_name="Bob",
            dob=date(1990, 11, 14),
            age=33.8,
            height=180,
            alive=True,
            active=False,
            last_acitve=datetime(2023, 10, 30, 10, 10, 10),
            period_active=datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1),
            current_time=time(18, 4, 12)
        )

        self.ma_desc = ma_resp_desc

    @classmethod
    def setUpClass(cls):
        """
        Start the client once before running any tests
        """
        cls.proc = Process(target=setup_server, args=(), daemon=True)
        cls.proc.start()
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleanup after the tests
        """
        cls.proc.terminate()
        cls.proc.join()

    def test_echo(self):
        """
        Test basic RPC with a simple echo
        """
        async def run_test():
            async with WebSocketRpcClient(uri, MAWaitingClient()) as client:
                text = "Hello World!"
                response = await client.other.echo(text=text)
                self.assertEqual(response.result, text)

        asyncio.run(run_test())
    
    def test_ping(self):
        """
        Test basic RPC with a simple ping
        """
        async def run_test():
            async with WebSocketRpcClient(uri, MAWaitingClient()) as client:
                try:
                    response = await client.other._ping_()
                    print(response)
                    passed = True
                except Exception as e:
                    logging.exception("Ping test failed")
                    passed = False
                assert passed

        asyncio.run(run_test())
    
    def test_server_calls(self):
        """
        Test basic RPC with a simple ping
        """
        async def run_test():
            async with WebSocketRpcClient(uri, MAWaitingClient()) as client:
                try:
                    #
                    passed = True
                except Exception as e:
                    logging.exception("Ping test failed")
                    passed = False
                assert passed

        asyncio.run(run_test())

    def test_get_server_hanlders(self):
        """
        Get registered handlers from server, compare to the 
        handlers we expect and the handlers we get client-side
        """
        async def run_test():
            async with WebSocketRpcClient(uri, MAWaitingClient()) as client:
                expected_handlers = ['gen_self_handlers', 'gen_other_handlers']
                """Making a call to the server to get it's registered handlers"""
                try:
                    response = await client.other.gen_self_handlers()

                except Exception as e:
                    logging.exception("Server handlers request failed")
                    logging.debug(e)

                server_handlers = response.result
                """Getting handlers registered on client"""
                try:
                    client_methods = await client.methods.gen_self_handlers()
                except Exception as e:
                    logging.exception("Client-side gen_self_handlers failed")
                    logging.debug(e)
                
                try:
                    """
                    Asking a server to make a call back call on client 
                    to get client-registerd handlers
                    """
                    remote_promise = await client.other.call_me_back(
                        method_name="gen_self_handlers", args={}
                    )

                    await asyncio.sleep(3)
                    try:
                        response = await client.other.get_response(
                            call_id=remote_promise.result
                        )
                    except Exception as e:
                        logging.exception("get_response from server failed")
                        logging.debug(e)

                except Exception as e:
                    logging.exception("call_me_back remote promise from client to server failed")
                    logging.debug(e)
                
                handlers_from_server = response.result['result']

                self.assertEqual(set(server_handlers), set(expected_handlers))
                self.assertEqual(set(client_methods), set(expected_handlers))
                self.assertEqual(set(handlers_from_server), set(expected_handlers))

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main() 