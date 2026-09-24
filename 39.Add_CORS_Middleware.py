from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


# ---------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------

# Origins are the frontend applications that are allowed
# to make browser requests to this FastAPI backend.
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,

    # Only these frontend origins are allowed to make
    # cross-origin requests to the API.
    allow_origins=origins,

    # Allows browsers to send credentials such as:
    # cookies, Authorization headers, etc.
    allow_credentials=True,

    # Allows all HTTP methods:
    # GET, POST, PUT, PATCH, DELETE, OPTIONS, etc.
    allow_methods=["*"],

    # Allows all request headers, such as:
    # Authorization, Content-Type, X-Custom-Header, etc.
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Data model
# ---------------------------------------------------------

class Item(BaseModel):
    name: str
    description: str = None


items = []


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/")
async def main():
    return {
        "message": "Hello World",
    }


@app.get("/items/")
def get_all_items():
    return items


@app.post("/items/")
def create_item():
    return {
        "name": "Foo",
        "description": "A very nice Item",
    }
