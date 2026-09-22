# Request Body - Following the Official FastAPI Tutorial
# Learn how to handle POST requests with data in the request body

from fastapi import FastAPI
from pydantic import BaseModel
# TODO: Import BaseModel from pydantic

app = FastAPI()

class Item(BaseModel):
    name:str
    description:str | None = None
    price:float 
    tax:float | None = None

@app.post("/items/")
def create_item(item:Item):
    return item

@app.post("/items/{item_id}")
def create_item_by_id(item_id:int ,item:Item):
    return {"item_id":item_id, **item.dict()}

