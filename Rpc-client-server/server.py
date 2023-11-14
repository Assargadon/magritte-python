import uvicorn
import asyncio
import random

from datetime import datetime
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, WebSocket
from fastapi_websocket_rpc.rpc_methods import RpcUtilityMethods
from fastapi_websocket_rpc.websocket_rpc_endpoint import WebsocketRPCEndpoint

from Magritte.descriptions.MAContainer_class import MAContainer
from Magritte.descriptions.MADateAndTimeDescription_class import MADateAndTimeDescription

from Magritte.visitors.MAJsonWriter_visitors import MAObjectJsonWriter, MAValueJsonWriter
from Magritte.visitors.MAStringSerializationVisitor import MAStringReaderVisitor


class MAWebsocketRPCEndpoint(WebsocketRPCEndpoint):
    pass


async def get_token_header(x_token: str = Header(...)):
    print(x_token)
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


def _deserialize_params(json_desc: str) -> MAContainer:
    """Convert json string into a MA model description"""
    json_reader = MAStringReaderVisitor()
    return json_reader.read_str(json_desc)

def _serialize_response(ma_output: MAContainer) -> str:
    """Convert MA model description into a json string"""
    json_writer = MAObjectJsonWriter(description=ma_output)
    json_desc = json_writer.write_json(ma_output)
    return json_desc

def _validate_model(ma_model) -> bool:
    pass


def serialization_decorator(func):
    def wrapper(*args, **kwargs):
        ma_desc = _deserialize_params(**kwargs)
        out = func(ma_desc)
        return _serialize_response(out)
    return wrapper


class MAConcatServer(RpcUtilityMethods):
    async def get_registered_handlers(self) -> list:
        asyncio.create_task(self.channel.other.allow_exit(delay=random.randint(1,4)))

        return [method for method in dir(self) if method.startswith('_') is False]

    async def get_user_status(self, person: str) -> str:
        asyncio.create_task(self.channel.other.allow_exit(delay=random.randint(1,4)))

        ma_desc = _deserialize_params(person)
        ma_user_status = MAContainer()

        ma_user_status += ma_desc[0]
        ma_user_status += ma_desc[7]
        ma_user_status += ma_desc[8]

        processing_timestamp = MADateAndTimeDescription(
            accessor='processing_timestamp',
            label='Processing timestamp',
            required=False,
            default=str(datetime.now())
        )
        ma_user_status += processing_timestamp

        json_resp = _serialize_response(ma_user_status)

        return json_resp

    async def call_callable(self, json_desc: str, callable: str):
        asyncio.create_task(self.channel.other.allow_exit(delay=random.randint(1,4)))

        ma_desc = _deserialize_params(json_desc)
        func_return = await getattr(self, callable)(ma_desc)

        return _serialize_response(func_return)


async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())