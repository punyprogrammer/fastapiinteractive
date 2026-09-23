# Schema Extra - Examples
# Provide example data for your API documentation.

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    # Field-level examples:
    # Provide example values for an individual field.
    name: str = Field(
        examples=["Laptop", "Smartphone"]
    )

    description: str | None = Field(
        default=None,
        examples=[
            "A powerful laptop",
            "Latest model smartphone",
        ],
    )

    price: float = Field(
        examples=[999.99, 499.99]
    )

    tax: float | None = Field(
        default=None,
        examples=[89.99, 44.99],
    )

    # Model-level examples:
    # Provide complete example objects for the entire request body.
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "description": "A powerful laptop",
                    "price": 999.99,
                    "tax": 89.99,
                }
            ]
        }
    }


# POST endpoint
# `response_model=Item` defines the shape of the response.
@app.post(
    "/items/",
    response_model=Item,
)
def create_item(item: Item):
    return item
