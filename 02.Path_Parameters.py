from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
def get_item(item_id):
    return {"item_id":item_id}

@app.get("/items/{item_id}/typed")
def get_item_typed(item_id:int):
    return {"item_id":item_id}

@app.get("/users/me")
def get_user():
        return {"user_id":"the current user"}

@app.get("/users/{user_id}")
def get_user_by_id(user_id:str):
    return {"user_id":user_id}
