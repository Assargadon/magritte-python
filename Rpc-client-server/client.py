"""
Я ожидаю примерно такое:
1) будет абстрактный класс MAWebsocketRouter и два его наследника, MAWebsocketClient и MAWebsocketServer.
2) у MAWebsocketClient будет метод .connect(...), а у MAWebsocketServer будет хендлер .onConnect
3) у MAWebsocketRouter будет метод .register_endpoint(endpointDescriptor, handler)
4) у того же MAWebsocketRouter будут методы

.get_my_endpoints()
и
.get_remote_endpoints()

RPC-роутер на основе fastapi-websocket-rpc

Первый шаг - сделать настройку, инкапсулирующую fastapi-websocket-rpc и предоставляющую 
функцию регистрацию обработчика, которому сообщают:
  - имя эндпойнта
  - список магритт-описателей параметров
  - магритт-описатель результата
  - callable с функцией-обработчиком (параметры которой должны идти в том же порядке, 
  что и описатели) 

Предполагается, что после этого сервер с такой надстройкой сможет:
  - выдать список зарегистрированных обработчиков
  - обеспечить вызов нужного обработчика (т.е. десериализовать переданные параметры, 
  вызвать функцию-обработчик и сериализовать её ответ)

Также, очевидно, потребуется веб-страничка, позволяющая протестировать вызов функций.  
Вторым шагом будет добавление в надстройку функции для вызова метода с другой стороны. 
Также, очевидно, потребуется какое-то АПИ для установки соединения (возможно хватит 
просто пробросить API из fastapi-websocket-rpc)

Третьим шагом будет валидация: параметров - со стороны исполнителя, и ответа - с 

вызывающей стороны. Потребуется поподробнее подумать над тем, что именно должно происходить, 
если валидация не прошла.

NB: эта задача НЕ использует сериализацию метаописателей, метаописатели просто создаются 
с обеих сторон.
RPC-роутер для REST-вызовов

Первым шагом будет система регистрации обработчиков, идентичная websocket-роутеру

Вторым - система для JSON-сериализации магриттовских дескрипторов. 
И добавление информации о них при запросе списка зарегистрированных обработчиков

Третьим, вероятно - генерация Swagger-интерфейса для зарегистрированных обработчиков.
"""
import asyncio
from os import wait

from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient, logger


logger.logging_config.set_mode(logger.LoggingModes.UVICORN, logger.logging.DEBUG)
PORT = 9000


class MAWebSocketRpcCLient(WebSocketRpcClient):
    pass


# Methods to expose to the clients
class WaitingClient(RpcMethodsBase):
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
    client = MAWebSocketRpcCLient(uri, WaitingClient())
    async with client:
        await client.channel.methods.can_send_queries.wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        run_client(f"ws://localhost:{PORT}/ws")
    )


'''
async def run_client(uri):
    async with MAWebSocketRpcCLient(uri, WaitingClient()) as client:
        # wait for the server to allow us to send questions
        await client.channel.methods.can_send_queries.wait()
        # call concat on the other side
        #response = await client.other.concat(a="hello", b=" world")

        #print(response.result)

        response = await client.other.get_registered_routes()
        print(response.result)
        # wait for the server to tell us we can exit
        response = await client.other.call_callable()
        print(response.result)

        await client.channel.methods.can_exit.wait()
'''