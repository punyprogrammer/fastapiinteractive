from enum import Enum
from typing import Any, Set, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


# POST endpoint for items
@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: Item) -> Item:
    return item


# `tags` groups endpoints in the generated OpenAPI/Swagger docs.
@app.get(
    "/items/",
    tags=["items"],
)
def get_items() -> list[dict[str, Any]]:
    return [{"name": "Foo", "price": 42}]


# Endpoints can belong to different documentation groups.
@app.get(
    "/users/",
    tags=["users"],
)
def get_users() -> list[dict[str, str]]:
    return [{"username": "johndoe"}]


# Tags can also be defined using an Enum.
@app.get(
    "/elements/",
    tags=[Tags.items],
)
def get_elements():
    return [{"item_id": "Foo"}]


# `summary` = short description displayed for the endpoint.
# `description` = detailed description of what the endpoint does.
@app.post(
    "/items-summary/",
    response_model=Item,
    summary="Create an item",
    description="This is the description for the created item.",
)
def create_item_summary(item: Item):
    return item


# The function docstring can also be used as the endpoint description.
# `summary` provides the short title shown in the API documentation.
@app.post(
    "/items-docstring/",
    response_model=Item,
    summary="Create an item",
)
def create_item_docstring(item: Item):
    """
    Create a new item.

    This endpoint accepts an Item and returns the
    created item using the Item response model.

    The response model ensures that the returned
    data follows the Item schema.
    """
    return item


# `deprecated=True` marks the endpoint as deprecated in OpenAPI docs.
# It tells API consumers that they should avoid using this endpoint.
@app.get(
    "/elements-deprecated/",
    tags=["items"],
    deprecated=True,
)
def get_deprecated_elements():
    return [{"item_id": "Foo"}]
