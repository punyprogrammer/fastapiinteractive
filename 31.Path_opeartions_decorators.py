from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
)


app = FastAPI()


# Dependency 1:
# Extract and validate the `X-Token` header.
async def verify_token(
    x_token: Annotated[str, Header()],
):
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=400,
            detail="X-Token header is invalid",
        )

    return x_token


# Dependency 2:
# Extract and validate the `X-Key` header.
async def verify_key(
    x_key: Annotated[str, Header()],
):
    if x_key != "fake-super-secret-key":
        raise HTTPException(
            status_code=400,
            detail="X-Key header is invalid",
        )

    return x_key


# Path operation decorator:
#
# `dependencies=[...]` tells FastAPI to execute these
# dependencies before executing the endpoint.
#
# The return values of the dependencies are NOT passed
# into `read_items()`.
#
# The dependencies are executed only for this route.
@app.get(
    "/items/",
    dependencies=[
        Depends(verify_token),
        Depends(verify_key),
    ],
)
async def read_items():
    return [
        {"item": "Foo"},
        {"item": "Bar"},
    ]
