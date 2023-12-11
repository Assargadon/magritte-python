
from fastapi import FastAPI
from pydantic import BaseModel


Item2_a = BaseModel.__annotations__.copy()
Item2_a["price"] = float

Item2 = type("Item2", 
              (BaseModel, ), 
              {
               "price": 0.0,
               #"__init__": Item2_init,
               "__annotations__": Item2_a,
               }
            )



app = FastAPI()


@app.post("/test/")
async def test(item: Item2):
    return item