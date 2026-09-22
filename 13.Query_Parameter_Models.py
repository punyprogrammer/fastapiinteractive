# Query Parameter Models
# FastAPI 0.115+ lets you group related query parameters
# into a single Pydantic model.

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    # Reject unexpected query parameters.
    model_config = {"extra": "forbid"}

    limit: int = Field(default=10)
    offset: int = Field(default=0)
    order_by: str = Field(default="created_at")


# Query() tells FastAPI to populate the model from query parameters.
@app.get("/items/")
def get_items(filter_query: FilterParams = Query()):
    return {
        "filters": filter_query.model_dump()
    }
