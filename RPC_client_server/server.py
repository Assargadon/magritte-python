from typing import Any

from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException

from Magritte.descriptions.MADescription_class import MADescription

from Magritte.visitors.MAJsonWriterReader_visitors import MAObjectJsonReader, MAObjectJsonWriter


async def get_token_header(x_token: str = Header(...)):
    print(x_token)
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def _deserialize_params(json_obj: str, desc: MADescription) -> Any:
    """Convert json string into an object using MA model description"""
    obj_decoder = MAObjectJsonReader()
    obj = obj_decoder.read_json(json_obj, desc)
    return obj

async def _serialize_response(obj: Any, desc: MADescription) -> str:
    """Convert an object into a json string using MA model description"""
    obj_encoder = MAObjectJsonWriter()
    json_obj = obj_encoder.write_json(obj, desc)
    return json_obj

def _validate_model(ma_model) -> bool:
    pass

'''
def serialization_decorator(func):
    def wrapper(*args, **kwargs):
        ma_desc = _deserialize_params(**kwargs)
        out = func(ma_desc)
        return _serialize_response(out)
    return wrapper
'''