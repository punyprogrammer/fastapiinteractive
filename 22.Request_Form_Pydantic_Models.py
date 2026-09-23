

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class RegistrationForm(BaseModel):
    username:str
    email:str
    password:str
    full_name:str | None = None 

@app.post("/register/")
def register_user(form_data:RegistrationForm = Form()):
    return {
        "message":"User registered",
        "username":form_data.username,
        "email":form_data.email
    }
