from fastapi import FastAPI

description = """

# Task Management API description here. 🚀
#
# ## Items
# Description of items functionality
#
# ## Users
# Description of users functionality


"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items/",
        },
    },
]
# TODO: Create FastAPI application with metadata
# Include: title, description, summary, version, terms_of_service,
# contact (name, url, email), license_info (name, url),
# and openapi_tags
app = FastAPI(
    title="Task Management API ",
    description=description,
    summary="A  simple and efficient task management application",
    version="1.0.0",
    terms_of_service="https://test-api.com",
     contact={
        "name": "API Support Team",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


@app.get("/")
async def root():
    """Root endpoint to verify the API is running."""
    return  {"message": "Welcome to Task Management API"}



@app.get("/items/",tags=["items"])
async def read_items():
    """Get all available items."""
    return [{"id": 1, "name": "Task Manager"}, {"id": 2, "name": "Code Editor"}]



# TODO: Add tags=["users"] to this endpoint
@app.get("/users/",tags={"users"})
async def read_users():
    """Get all users."""
    return  [{"username": "johndoe"}, {"username": "janedoe"}]

