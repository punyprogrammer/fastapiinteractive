from fastapi import FastAPI, Query

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# Query() lets you configure and validate query parameters.
#
# Common options:
# - default: Default value when the parameter is omitted
# - min_length / max_length: String length constraints
# - ge / le: Numeric >= / <= constraints
# - gt / lt: Numeric > / < constraints
# - description: Adds documentation to the OpenAPI/Swagger UI
#
# Examples:
# Query(default=None, max_length=50)
# Query(min_length=3, max_length=50)
# Query(10, ge=1, le=100)


@app.get("/items/")
def get_items(
    q: str | None = Query(default=None, max_length=50)
):
    if q:
        return list(
            filter(
                lambda x: q.casefold() in x["item_name"].casefold(),
                fake_items_db
            )
        )

    return fake_items_db


@app.get("/items/search/")
def search_items(
    skip: int = 0,
    q: str = Query(
        min_length=3,
        max_length=50,
        description="Search Query"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of items"
    ),
):
    filtered_results = list(
        filter(
            lambda x: q.casefold() in x["item_name"].casefold(),
            fake_items_db
        )
    )

    if not filtered_results:
        return []

    return {
        "query": q,
        "limit": limit,
        "results": filtered_results[skip:skip + limit]
    }
