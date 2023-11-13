import logging
import json
import os
import sys

import asyncio
from multiprocessing import Process
import uvicorn

from fastapi import FastAPI
import unittest
from datetime import datetime, timedelta, date, time
from client import MAWebSocketRpcCLient, WaitingClient
from server import MAWebsocketRPCEndpoint, MAConcatServer, _serialize_response, _deserialize_params

from descriptions.MAStringDescription_class import MAStringDescription
from descriptions.MAElementDescription_class import MAElementDescription
from descriptions.MADateDescription_class import MADateDescription
from descriptions.MATimeDescription_class import MATimeDescription
from descriptions.MAIntDescription_class import MAIntDescription
from descriptions.MABooleanDescription_class import MABooleanDescription
from descriptions.MAFloatDescription_class import MAFloatDescription
from descriptions.MADurationDescription_class import MADurationDescription
from descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription
from descriptions.MAReferenceDescription_class import MAReferenceDescription
from descriptions.MAContainer_class import MAContainer

from visitors.MAJsonWriter_visitors import MAObjectJsonWriter, MAValueJsonWriter


# Configurable
PORT = "8080"
uri = f"ws://localhost:{PORT}/ws"

first_name_desc = MAStringDescription(
            name='first_name', 
            label='First name', 
            default='Paul'
        )

date_of_birth = MADateDescription(
            name='dob', 
            label='Birth date', 
            default=date(1990, 1, 1)
        )

last_active = MADateAndTimeDescription(
            name='last_active',
            label='Last time active',
            default=datetime(2023, 10, 30, 10, 10, 10),
        )

current_time = MATimeDescription(
            name='current_time',
            label='Current time',
            default=time(18, 4, 12)
        )

height = MAIntDescription(
            name='height', 
            label='height', 
            default=180
        )

age = MAFloatDescription(name='age', label='age', default=33.5)
alive = MABooleanDescription(
            name='alive', 
            label='alive', 
            default=True
        )

active = MABooleanDescription(
            name='active', 
            label='active', 
            default=False
        )

period_active = MADurationDescription(
            name='period_active', 
            label='period_active', 
            default=datetime(2023,2,1,14,0)-datetime(2023,3,8,16,1)
        )
'''
ref = MAReferenceDescription(
            accessor = "obj", 
            reference = model, 
            required = False
        )
'''
height_desc = MAIntDescription(
            name = "height", 
            undefined='-',
            default='-'
        )

processing_timestamp = MADateAndTimeDescription(
            name='processing_timestamp',
            label='Processing timestamp',
            default=datetime.now()
        )

ma_desc = MAContainer()
ma_desc.label = "Test Request description"
ma_desc += first_name_desc
ma_desc += date_of_birth
ma_desc += last_active
ma_desc += current_time
ma_desc += height
ma_desc += age
ma_desc += alive
ma_desc += active
ma_desc += period_active
ma_desc += height_desc

ma_resp_test = MAContainer()
ma_resp_test.label = "Test Response description"
ma_resp_test += first_name_desc
ma_resp_test += active
ma_resp_test += period_active
ma_resp_test += processing_timestamp

json_desc = json.dumps({
    "label": "Test Request description",
    "elements": [
        {
            "accessor": "first_name",
            "label": "First name",
            "required": False,
            "default": "Paul"
        },
        {
            "accessor": "dob",
            "label": "Birth date",
            "required": False,
            "default": "1990-01-01"
        },
        {
            "accessor": "last_active",
            "label": "Last time active",
            "required": False,
            "default": "2023-10-30T10:10:10"
        },
        {
            "accessor": "current_time",
            "label": "Current time",
            "required": False,
            "default": "18:04:12"
        },
        {
            "accessor": "height",
            "label": "height",
            "required": False,
            "default": 180
        },
        {
            "accessor": "age",
            "label": "age",
            "required": False,
            "default": 33.5
        },
        {
            "accessor": "alive",
            "label": "alive",
            "required": False,
            "default": True
        },
        {
            "accessor": "active",
            "label": "active",
            "required": False,
            "default": False
        },
        {
            "accessor": "period_active",
            "label": "period_active",
            "required": False,
            "default": "2023-03-08T16:01:00"
        },
        {
            "accessor": "height_desc",
            "label": "height_desc",
            "required": False,
            "default": "-"
        }
    ]    
})

json_resp = json.dumps({
    "label": "Test Response description",
    "elements": [
        {
            "accessor": "first_name",
            "label": "First name",
            "required": False,
            "default": "Paul"
        },
        {
            "accessor": "active",
            "label": "active",
            "required": False,
            "default": False
        },
        {
            "accessor": "period_active",
            "label": "period_active",
            "required": False,
            "default": "2023-03-08T16:01:00"
        },
        {
            "accessor": "processing_timestamp",
            "label": "Processing timestamp",
            "required": False,
            "default": "2023-03-08T16:01:00"
        }
    ]    
})


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


def setup_server():
    app = FastAPI()
    endpoint = MAWebsocketRPCEndpoint(MAConcatServer())
    endpoint.register_route(app)

    uvicorn.run(app, port=PORT)


class TestRPCMethods(unittest.TestCase):
    def setUp(self):
        self.func_name = 'test_handler_func' 
        self.handler_name = 'person_handler'
        self.mg_params = ()

        self.model = TestPerson(
            first_name="Bob", 
            dob=str(date(1990, 11, 14)), 
            age="33.8", 
            height="180", 
            alive="True",
            active="False",
            last_acitve=str(datetime(2023, 10, 30, 10, 10, 10)),
            period_active="30 days, 0:00:00",
            current_time="18:04:12"
        )

        self.ma_desc = ma_desc

    @classmethod
    def setUpClass(cls):
        # Start the client once before running any tests
        cls.proc = Process(target=setup_server, args=(), daemon=True)
        cls.proc.start()
    
    @classmethod
    def tearDownClass(cls):
        # Cleanup after the test
        cls.proc.terminate()
        cls.proc.join()
    
    def test_echo(self):
        """
        Test basic RPC with a simple echo
        """
        async def run_test():
            async with MAWebSocketRpcCLient(uri, MAConcatServer(), default_response_timeout=4) as client:
                text = "Hello World!"
                response = await client.other.echo(text=text)
                self.assertEqual(response.result, text)

        asyncio.run(run_test())
    
    def test_ping(self):
        """
        Test basic RPC with a simple ping
        """
        async def run_test():
            async with MAWebSocketRpcCLient(uri, MAConcatServer(), default_response_timeout=4) as client:
                try:
                    response = await client.other._ping_()
                    print(response)
                    passed = True
                except Exception as e:
                    logging.exception("Ping test failed")
                    passed = False
                assert passed

        asyncio.run(run_test())

    """
    Выдать список зарегистрированных обработчиков
    """
    def test_get_remote_handlers(self):
        async def run_test():
            async with MAWebSocketRpcCLient(uri, MAConcatServer(), default_response_timeout=4) as client:
                response = await client.other.get_registered_handlers()

                #logging.debug(response)

                attrs = (
                    'get_registered_handlers', 'call_callable', 
                    'get_user_status', 'get_process_details',
                    'call_me_back', 'get_response', 'echo', 
                    'channel'
                )

                assert response

        asyncio.run(run_test())


    def test_self_handlers(self):
        async def run_test():
            pass
        asyncio.run(run_test())

    """
    Обеспечить вызов нужного обработчика (т.е. десериализовать переданные параметры, 
    вызвать функцию-обработчик и сериализовать её ответ)
    """
    def test_call_callable(self):
        async def run_test():
            async with MAWebSocketRpcCLient(uri, MAConcatServer(), default_response_timeout=4) as client:
                #try:
                    logging.debug(self.func_name)
                    json_model = await _serialize_response(ma_output=ma_desc)

                    #assert json_model == json_desc
        
                    response = await client.other.get_user_status(person=json_model)

                    #assert response == json_resp

                    ma_resp = await _deserialize_params(json_desc=response)

                    #assert ma_resp == ma_resp_test
                #except Exception as e:
                #    logging.exception("Call handler failed")
                #    response = False
                    assert response

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()

'''
class MATestServer(unittest.TestCase):
    def setUp(self):
        pass
    
    async def concat(sel):
        pass

    async def test_get_self_handlers(self):
        #response = client.other.get_registered_handlers()
        pass

    async def test_get_remote_handlers(self):
        #response = client.other.get_registered_handlers()
        pass

    async def test_call_callable(self):
        #response = client.other.call_callable()
        pass
'''