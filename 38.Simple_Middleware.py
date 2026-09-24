import time

from fastapi import FastAPI, Request
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None


# Sample data
items = {
    "foo": {
        "name": "The Foo Wrestlers",
    },
    "bar": {
        "name": "The Bar Tenders",
    },
}


# Middleware receives:
# 1. request  -> incoming HTTP request
# 2. call_next -> passes the request to the next middleware/endpoint
@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    # Continue processing the request
    response = await call_next(request)

    # Calculate total request processing time
    process_time = time.perf_counter() - start_time

    # Add custom response header
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.get("/")
async def read_root():
    return {
        "message": "Hello World",
    }


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id in items:
        return items[item_id]

    return {
        "error": "Item not found",
    }


@app.post("/items/")
async def create_item():
    return {
        "id": "item_3",
        "name": "test item",
        "description": "A test item",
    }
