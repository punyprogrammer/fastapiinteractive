from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()


# Pydantic model
class Item(BaseModel):
    name: str
    price: float


# Simple in-memory database
items_db: dict[int, Item] = {}
next_id = 1


# Simulated database session
class DBSession:
    def __init__(self):
        self.connected = True
        self.transaction_count = 0
        print("Database connection established")

    def close(self):
        self.connected = False
        print("Database connection closed")


# Database dependency
async def get_db():
    db = DBSession()

    try:
        yield db
    finally:
        db.close()


# Create item
@app.post("/items/")
def create_item(
    item: Item,
    db: Annotated[DBSession, Depends(get_db)]
):
    global next_id

    db.transaction_count += 1

    item_id = next_id
    items_db[item_id] = item

    next_id += 1

    return {
        "id": item_id,
        "name": item.name,
        "price": item.price,
        "message": "Item created with database session cleanup"
    }


# Get all items
@app.get("/items/")
def get_items(
    db: Annotated[DBSession, Depends(get_db)]
):
    return [
        {
            "id": item_id,
            "name": item.name,
            "price": item.price
        }
        for item_id, item in items_db.items()
    ]
