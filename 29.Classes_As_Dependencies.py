from fastapi import FastAPI, Depends
from typing import Annotated


app = FastAPI()


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


# Dependency class
#
# FastAPI will create an instance of this class and provide
# the query parameters from the request to __init__().
class CommonQueryParams:
    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        # Store the resolved query parameters as instance attributes.
        self.q = q
        self.skip = skip
        self.limit = limit


# GET /items/
#
# Depends() without an argument tells FastAPI to use the
# type specified in Annotated:
#
#     CommonQueryParams
#
# FastAPI effectively creates:
#
#     CommonQueryParams(q=..., skip=..., limit=...)
#
# and injects the resulting object into `commons`.
@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()],
):
    # Create the response dictionary.
    response = {}

    # Add `q` only if the client provided it.
    if commons.q:
        response["q"] = commons.q

    # Slice the database using skip and limit.
    items_slice = fake_items_db[
        commons.skip : commons.skip + commons.limit
    ]

    response["items"] = items_slice

    return response


# GET /users/
#
# Explicit dependency syntax:
#
# Depends(CommonQueryParams)
#
# This explicitly tells FastAPI which dependency to execute.
@app.get("/users/")
async def read_users(
    commons: Annotated[
        CommonQueryParams,
        Depends(CommonQueryParams),
    ],
):
    response = {}

    if commons.q:
        response["q"] = commons.q

    items_slice = fake_items_db[
        commons.skip : commons.skip + commons.limit
    ]

    response["items"] = items_slice

    return response
