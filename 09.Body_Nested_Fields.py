from typing import Dict, List, Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class Item(ItemBase):
    tags: set[str] = set()
    image: Image | None = None


class ItemWithImages(ItemBase):
    images: list[Image] = []


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item": item
    }


@app.put("/items/{item_id}/images")
def update_item_with_images(item_id: int, item: ItemWithImages):
    return {
        "item_id": item_id,
        "item": item
    }


@app.post("/index-weights/")
def create_index_weights(weights: Dict[int, float]):
    return weights
