import asyncio
import logging
import sys
from typing import Any

from fastapi import FastAPI
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint, WebSocketRpcClient
from fastapi_websocket_rpc.rpc_methods import RpcUtilityMethods

from Magritte.descriptions.MADescription_class import MADescription
from Magritte.visitors.MAJsonWriterReader_visitors import MAObjectJsonReader, MAObjectJsonWriter


async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())


class MAWebSocketRpcBase(RpcUtilityMethods):
    """Base methods shared by both the client and server"""
    async def _deserialize_params(json_obj: str, desc: MADescription) -> Any:
        """Convert json string into an object using MA model description"""
        obj_decoder = MAObjectJsonReader()
        obj = obj_decoder.read_json(json_obj, desc)
        return obj

    async def _serialize_response(obj: Any, desc: MADescription) -> str:
        """Convert an object into a json string using MA model description"""
        obj_encoder = MAObjectJsonWriter()
        json_desc = obj_encoder.write_json(obj, desc)
        return json_desc

    async def gen_self_handlers(self) -> list:
        self_handlers = [method for method in dir(self) if method.startswith('gen_')]
        return self_handlers

    async def gen_other_handlers(self) -> list:
        other_handlers = await self.other.gen_self_handlers()
        return other_handlers
