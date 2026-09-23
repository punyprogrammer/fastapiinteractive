# Header Parameter Models
# FastAPI 0.115+ lets you group related headers
# into a single Pydantic model.

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    # Required header.
    x_token: str

    # Optional header.
    x_request_id: str | None = None

    # Default value when the header is not provided.
    accept_language: str = "en"


# Header() tells FastAPI to populate the model from HTTP headers.
@app.get("/info/")
def get_info(headers: CommonHeaders = Header()):
    return {
        "headers": headers.model_dump()
    }
