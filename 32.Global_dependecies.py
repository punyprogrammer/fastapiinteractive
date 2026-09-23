# 📚 Theory — Global Dependencies
#
# Global dependencies are applied to the entire FastAPI application.
# `FastAPI(dependencies=[...])` runs them automatically for EVERY
# path operation in the application.
#
# Useful for cross-cutting concerns such as authentication,
# authorization, API-key validation, etc.
#
# Advantage: avoids repeating the same dependencies on every endpoint.
#
# Keep global dependencies lightweight to minimize performance overhead.
#
# Dependencies can also be applied to groups of path operations
# when structuring larger applications.

from typing_extensions import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


# Dependency: validate the X-Token header.
async def verify_token(
    x_token: Annotated[str, Header()],
):
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=400,
            detail="The X-Token header is not valid",
        )


# Dependency: validate the X-Key header.
async def verify_key(
    x_key: Annotated[str, Header()],
):
    if x_key != "fake-super-secret-key":
        raise HTTPException(
            status_code=400,
            detail="The X-Key header is not valid",
        )


# Application-level dependencies:
# These run automatically before EVERY path operation.
app = FastAPI(
    dependencies=[
        Depends(verify_token),
        Depends(verify_key),
    ]
)


@app.get("/items/")
async def read_items():
    return [
        {"item": "Portal Gun"},
        {"item": "Plumbus"},
    ]


@app.get("/users/")
async def read_users():
    return [
        {"username": "Rick"},
        {"username": "Morty"},
    ]
