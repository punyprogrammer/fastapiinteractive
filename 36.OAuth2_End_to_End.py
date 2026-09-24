```python
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing_extensions import Annotated


# Fake users database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


app = FastAPI()


# Fake password hashing function for demonstration.
def fake_hash_password(password: str):
    return "fakehashed" + password


# Extracts the Bearer token from the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: Union[bool, None] = None


class UserInDB(User):
    # Contains sensitive fields that shouldn't be returned to clients.
    hashed_password: str


def get_user(db, username: str):
    """Look up a user by username."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    # In this demo, the token is simply the username.
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    # OAuth2PasswordBearer extracts the token from:
    # Authorization: Bearer <token>
    user = fake_decode_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Reject disabled users.
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # OAuth2PasswordRequestForm extracts username/password
    # from application/x-www-form-urlencoded request data.
    user = get_user(fake_users_db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    # Demo only: the username is being used as the access token.
    return {
        "access_token": user.username,
        "token_type": "bearer",
    }


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # FastAPI resolves get_current_user() automatically.
    return current_user
```
