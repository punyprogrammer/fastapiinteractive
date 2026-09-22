from typing import Union

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


# Mix path, query, and body parameters.
@app.put("/items/{item_id}/basic")
def get_item_by_id_basic(
    item_id: int = Path(
        title="The ID of the item to get",
        ge=0,
        le=1000
    ),
    q: str | None = None,
    item: Item | None = None,
):
    return {
        "item_id": item_id,
        **({"q": q} if q else {}),
        **({"item": item} if item else {}),
    }


# Multiple Pydantic models are automatically treated as body parameters.
@app.put("/items/{item_id}")
def put_item_by_id(
    item_id: int,
    item: Item,
    user: User
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user
    }


# Body() makes a singular value part of the request body.
@app.put("/items/{item_id}/importance")
def put_item_by_importance(
    item_id: int,
    item: Item,
    user: User,
    importance=Body()
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }


# * makes all following parameters keyword-only.
# Useful for keeping long parameter lists readable and avoiding positional arguments.
@app.put("/items/{item_id}/full")
def put_items_by_id_full(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: str | None = None
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
        **({"q": q} if q else {}),
    }


# embed=True wraps a single body parameter inside a key.
# Without embed=True:
# {"name": "Foo", "price": 42}
#
# With embed=True:
# {"item": {"name": "Foo", "price": 42}}
@app.put("/items/{item_id}/embed")
def put_item_by_item_id_embed(
    item_id: int,
    item: Item = Body(embed=True)
):
    return {
        "item_id": item_id,
        "item": item
    }
