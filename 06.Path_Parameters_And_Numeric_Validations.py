from fastapi import FastAPI, Path, Query

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# Path() validates and adds metadata to path parameters.
# Common options: ge/le, gt/lt, min_length/max_length, title, description.
# Path parameters are always required because they are part of the URL.
#
# NOTE: When a function has both Path() and Query() parameters,
# define Path() parameters before Query() parameters.

@app.get("/items/{item_id}")
def get_item_by_id(
    item_id: int = Path(ge=1)
):
    return {"item_id": item_id}


@app.get("/items/{item_id}/details")
def get_item_details(
    # Path parameter: 1 <= item_id <= 1000
    item_id: int = Path(
        ge=1,
        le=1000,
        description="The ID of the item"
    ),
    # Optional query parameter
    q: str | None = Query(
        default=None,
        max_length=50
    ),
):
    return {
        "item_id": item_id,
        "q": q,
        "details": "Item details here"
    }


@app.get("/users/{user_id}")
def get_user_by_id(
    user_id: int = Path(
        title="User ID",
        description="The ID of the user to get",
        ge=1
    )
):
    return {
        "user_id": user_id,
        "message": f"User {user_id} profile"
    }
