from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .routers import items, users
from .internal import admin


# Applied to every endpoint in the application.
app = FastAPI(
    dependencies=[
        Depends(get_query_token),
    ]
)


# Register application routers.
app.include_router(users.router)

app.include_router(items.router)


# Admin router with its own prefix, tags, dependency,
# and additional documented response.
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[
        Depends(get_token_header),
    ],
    responses={
        418: {
            "description": "I'm a teapot",
        }
    },
)


@app.get("/")
async def root():
    return {
        "message": "Hello Bigger Applications!"
    }
