from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()


# Serve files from the local "static" directory
# through the "/static" URL path.
#
# Example:
# static/index.html
#       ↓
# http://localhost:8000/static/index.html
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get("/")
async def root():
    return  {
  "message": "FastAPI Static Files Demo",
  "docs": "/docs",
  "static_demo": "/static/index.html"
}
