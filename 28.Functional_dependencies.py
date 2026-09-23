from typing import Annotated

from fastapi import Depends, FastAPI


app = FastAPI()


# Dependency function
#
# FastAPI calls this function automatically when an endpoint
# declares it using Depends().
#
# The parameters `q`, `skip`, and `limit` are extracted from
# the request query parameters.
async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
    }


# `Depends(common_parameters)` tells FastAPI:
#
# 1. Call common_parameters() before executing this endpoint.
# 2. Resolve its parameters (`q`, `skip`, `limit`).
# 3. Pass the returned dictionary into `commons`.
#
# `Annotated` combines the Python type (`dict`) with
# FastAPI dependency metadata (`Depends(...)`).
@app.get("/items/")
async def read_items(
    commons: Annotated[
        dict,
        Depends(common_parameters),
    ],
):
    return commons


# The same dependency can be reused by multiple endpoints.
@app.get("/users/")
async def read_users(
    commons: Annotated[
        dict,
        Depends(common_parameters),
    ],
):
    return commons
