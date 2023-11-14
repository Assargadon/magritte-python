import uvicorn
import asyncio
import random
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, WebSocket

from server import MAWebsocketRPCEndpoint, MAConcatServer


async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())

app =  FastAPI()
endpoint = MAWebsocketRPCEndpoint(MAConcatServer(), on_connect=[on_connect])
endpoint.register_route(app)

uvicorn.run(app, host="0.0.0.0", port=9000)