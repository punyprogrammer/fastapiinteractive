# 🔧 Key Concepts
# `jsonable_encoder` converts Pydantic models and other Python data types
# into JSON-compatible Python data structures.
#
# Database Storage:
# Many databases expect JSON-compatible data structures.
#
# DateTime Handling:
# Converts `datetime` objects into ISO-formatted strings.
#
# Dictionary Conversion:
# Converts Pydantic models into plain Python dictionaries.
#
# 💡 Best Practices
# - Use `jsonable_encoder` when storing Pydantic models in databases.
# - Convert `datetime` and other non-JSON-compatible types before serialization.
# - `jsonable_encoder` returns Python data structures, NOT a JSON string.
# - The result can be passed to Python's standard `json.dumps()`.

from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    # Convert the Pydantic model into JSON-compatible Python data.
    json_encoded = jsonable_encoder(item)

    # Store the JSON-compatible data in the database.
    fake_db[id] = json_encoded

    return json_encoded
