import uvicorn
import asyncio
from functools import partial
from abc import ABC

from typing import List, Dict, Union, Optional
from fastapi import FastAPI
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint, WebSocketRpcClient

from Magritte.Magritte.descriptions.MADescription_class import MADescription
from Magritte.Magritte.descriptions.MAPriorityContainer_class import MAPriorityContainer
from Magritte.Magritte.visitors.MAJsonWriter_visitors import MAValueJsonWriter, MAObjectJsonWriter
from Magritte.Magritte.visitors.MAStringWriterReader_visitors import MAStringReaderVisitor, MAStringWriterVisitor
'''
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
'''


async def on_connect(channel):
    await asyncio.sleep(1) 
    # now tell the client it can start sending us queries
    asyncio.create_task(channel.other.allow_queries())


class MAWebsocketRouter(ABC):

    def __init__(
            self, app: FastAPI, path: str, 
            mg_params: List[MADescription], 
            mg_output: MAPriorityContainer
    ):
        self.app = app
        self.path = path
        self.mg_params = mg_params
        self.mg_output = mg_output

    def get_my_endpoints(self):
        pass

    def get_remote_endpoints(self):
        pass
