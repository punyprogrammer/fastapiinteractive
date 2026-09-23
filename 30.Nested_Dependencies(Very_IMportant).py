from typing import Annotated

from fastapi import Cookie, Depends, FastAPI


app = FastAPI()


# Dependency 1:
# Extracts the `q` query parameter from the request.
def query_extractor(
    q: str | None = None,
):
    return q


# Dependency 2:
# Depends on `query_extractor`.
#
# FastAPI first resolves `query_extractor` to obtain `q`,
# then passes that value into this function.
#
# `last_query` is read from the request's cookie.
def query_or_cookie_extractor(
    q: Annotated[
        str | None,
        Depends(query_extractor),
    ],
    last_query: Annotated[
        str | None,
        Cookie(),
    ] = None,
):
    # If no query parameter was provided,
    # fall back to the `last_query` cookie.
    if not q:
        return last_query

    # If q exists, prefer it over the cookie.
    return q


# Endpoint:
# Depends on query_or_cookie_extractor.
#
# FastAPI resolves the entire dependency chain automatically.
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[
        str | None,
        Depends(query_or_cookie_extractor),
    ],
):
    return {
        "q_or_cookie": query_or_default,
    }
