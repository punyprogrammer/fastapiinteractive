# Exception Handling
#
# FastAPI provides:
# - HTTPException → Raise standard HTTP errors from an endpoint.
# - Custom exception handlers → Define custom behavior for
#   application-specific exceptions.

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {
    "foo": "The Foo Wrestlers"
}


# HTTPException
# Use HTTPException when an endpoint needs to return an HTTP error.
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return {
        "item": items[item_id]
    }


# HTTPException with custom headers.
# Headers can provide additional information to the client.
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={
                "X-Error": "There goes my error"
            },
        )

    return {
        "item": items[item_id]
    }


# Custom application exception.
# Custom exceptions are useful when your application has
# domain-specific errors that need custom handling.
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# Custom exception handler.
# Whenever UnicornException is raised, FastAPI calls this handler
# instead of returning the default unhandled-exception response.
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(
    request: Request,
    exc: UnicornException,
):
    return JSONResponse(
        status_code=418,
        content={
            "message": "Error with unicorn",
            "unicorn_name": exc.name,
        },
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)

    return {
        "unicorn_name": name
    }
