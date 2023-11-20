import asyncio
from fastapi_websocket_rpc import WebSocketRpcClient, logger

from RPC_client_server.rpc_handler import MAWebSocketRpcBase


logger.logging_config.set_mode(logger.LoggingModes.UVICORN, logger.logging.DEBUG)
PORT = 9000


# Methods to expose to the clients
class MAWaitingClient(MAWebSocketRpcBase):
    def __init__(self):
        super().__init__()
        self.can_send_queries = asyncio.Event()
        self.can_exit = asyncio.Event()


    async def allow_queries(self):
        self.can_send_queries.set()
        return None

    async def allow_exit(self, delay):
        async def allow():
            await asyncio.sleep(delay)
            self.can_exit.set()
        asyncio.create_task(allow())


async def run_client(uri):
    client = WebSocketRpcClient(uri, MAWaitingClient())
    async with client:
        await client.channel.methods.can_send_queries.wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        run_client(f"ws://localhost:{PORT}/ws")
    )
