
from typing import Any
from Magritte.visitors.MAReferencedDataWriterReader_visitors import MAReferencedDataHumanReadableSerializer, MAReferencedDataHumanReadableDeserializer
from fastapi import FastAPI
from pydantic import BaseModel


class MAModelFastapiAdapterDTO(BaseModel):
    serialized_str: str

    @staticmethod
    def describe(request_descriptor, response_descriptor):
        def describe_decorator(callback):
            async def wrapper_decorator():
                return await callback()
            return wrapper_decorator
        return describe_decorator

if __name__ == "__main__":
    import uvicorn
    app = FastAPI()

    @app.get("/", response_model=MAModelFastapiAdapterDTO)
    @MAModelFastapiAdapterDTO.describe(request_descriptor=1, response_descriptor=2)
    async def index():
        response = MAModelFastapiAdapterDTO(serialized_str='Z')
        return response

    @app.post("/test", response_model=MAModelFastapiAdapterDTO)
    async def test(request: MAModelFastapiAdapterDTO):
        return request

    uvicorn.run(app, host="0.0.0.0", port=8000)

