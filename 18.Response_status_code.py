# Response Status Code
# Learn how to specify HTTP status codes for your API responses
from fastapi import FastAPI,status
app = FastAPI()
@app.post("/items/",status_code = status.HTTP_201_CREATED)
def create_item(name:str):
    return {
        "name":name
    }
