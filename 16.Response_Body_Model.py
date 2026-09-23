# Response Models
# Response models define and validate the data returned by an API.
#
# They can be declared using:
# 1. A return type annotation: -> Item
# 2. The response_model parameter: response_model=Item
#
# Key benefits:
# - Validation: Ensures returned data matches the expected schema.
# - Security: Helps prevent accidental exposure of internal/sensitive fields.
# - Filtering: Only fields defined in the response model are included.
# - Documentation: Generates the response schema in OpenAPI/Swagger UI.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# -> Item tells FastAPI to validate and serialize the response
# according to the Item model.
#
# Security:
# - Prevents accidental exposure of fields not defined in Item.
#
# Filtering:
# - Only fields declared in Item are included in the response.
@app.post("/items/")
def create_item(item: Item) -> Item:
    return item


# -> list[Item] declares that the response must be a list
# containing Item objects.
#
# Security:
# - Internal fields returned by the database/business logic
#   can be excluded from the public API response.
#
# Filtering:
# - Only fields defined in Item are included for each item.
@app.get("/items/")
def get_items() -> list[Item]:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
