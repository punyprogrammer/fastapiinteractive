# Extra Models
# Use multiple related Pydantic models when different API layers
# need different representations of the same resource.
#
# Common pattern:
# UserBase  → Shared public fields
# UserIn    → Data accepted from the client
# UserOut   → Data returned to the client
# UserInDB  → Internal/database representation

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# Shared fields used by multiple User models.
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# Input model:
# Contains fields that the client is allowed to send.
class UserIn(UserBase):
    password: str


# Output model:
# Contains only fields that the API is allowed to return.
class UserOut(UserBase):
    pass


# Internal/DB model:
# Contains sensitive/internal fields that should not be exposed publicly.
class UserInDB(UserBase):
    hashed_password: str


async def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


async def fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_password = await fake_password_hasher(user_in.password)

    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )

    print("User saved! ..not really")

    return user_in_db


# response_model controls the actual response sent to the client.
#
# Even though fake_save_user() returns UserInDB, which contains
# hashed_password, response_model=UserOut filters that field
# from the API response.
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn) -> UserOut:
    user_saved = await fake_save_user(user_in)
    return user_saved
