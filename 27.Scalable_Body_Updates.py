from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5


# Simulated database
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    """Get an item by ID."""

    # Check if item exists.
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item_with_put(item_id: str, item: Item):
    """Update an item completely (full replacement)."""

    # Check if item exists.
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    # Convert Pydantic model to JSON-compatible dictionary.
    json_encoded_item = jsonable_encoder(item)

    # Replace the existing item completely.
    items[item_id] = json_encoded_item

    return json_encoded_item


@app.patch("/items/{item_id}", response_model=Item)
async def update_item_with_patch(item_id: str, item: Item):
    """Update an item partially (only provided fields)."""

    # Check if item exists.
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    # Convert the stored dictionary into a Pydantic model.
    stored_item_model = Item(**items[item_id])

    # Get only fields explicitly provided by the client.
    update_data = item.dict(exclude_unset=True)

    # Create a new model with the updated fields.
    updated_item = stored_item_model.copy(update=update_data)

    # Convert the updated model to a JSON-compatible dictionary.
    json_encoded_item = jsonable_encoder(updated_item)

    # Store the updated item.
    items[item_id] = json_encoded_item

    return updated_item
