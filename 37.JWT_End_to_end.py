from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# -------------------------------------------------------------------
# Fake users database
# -------------------------------------------------------------------

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# Extracts the Bearer token from:
# Authorization: Bearer <JWT>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# -------------------------------------------------------------------
# Pydantic models
# -------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: Union[None, bool]


class UserInDB(User):
    hashed_password: str


# -------------------------------------------------------------------
# Password helpers
# -------------------------------------------------------------------

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def get_password_hash(password):
    return pwd_context.hash(password)


# -------------------------------------------------------------------
# User helpers
# -------------------------------------------------------------------

def get_user(db, username: str):
    if username not in db:
        raise HTTPException(
            status_code=400,
            detail="The user does not exist",
        )

    return db[username]


def authenticate_user(fake_db, username: str, password: str):
    if username not in fake_db:
        return False

    user = UserInDB(**fake_db[username])

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return False

    return user


# -------------------------------------------------------------------
# JWT helpers
# -------------------------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None,
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# -------------------------------------------------------------------
# Dependency 1: Extract and validate the JWT
# -------------------------------------------------------------------

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        # oauth2_scheme extracts the token from:
        #
        # Authorization: Bearer <JWT>
        #
        # Then we verify the JWT signature and expiration.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # The username was stored in the JWT when we created it:
        #
        # {"sub": user.username}
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Use the username from the verified JWT
        # to retrieve the actual user.
        user = get_user(
            fake_users_db,
            username,
        )

        return User(**user)

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# -------------------------------------------------------------------
# Dependency 2: Validate that the user is active
# -------------------------------------------------------------------

async def get_current_active_user(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    # FastAPI automatically calls get_current_user()
    # before calling this dependency.
    #
    # Dependency chain:
    #
    # get_current_active_user
    #          ↓
    # get_current_user
    #          ↓
    # oauth2_scheme
    #          ↓
    # Authorization: Bearer <JWT>

    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user


# -------------------------------------------------------------------
# Login endpoint
# -------------------------------------------------------------------

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
):
    # OAuth2PasswordRequestForm extracts:
    #
    # username
    # password
    #
    # from the POST form body.

    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    # Create JWT containing:
    #
    # {
    #     "sub": "johndoe",
    #     "exp": <expiration>
    # }
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# -------------------------------------------------------------------
# Protected endpoint: Current user
# -------------------------------------------------------------------

@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[
        User,
        Depends(get_current_active_user),
    ],
):
    # FastAPI automatically resolves the entire dependency chain:
    #
    # HTTP request
    #      ↓
    # Authorization: Bearer <JWT>
    #      ↓
    # oauth2_scheme
    #      ↓
    # get_current_user
    #      ↓
    # JWT verification
    #      ↓
    # Extract "sub" from JWT
    #      ↓
    # Fetch user from database
    #      ↓
    # get_current_active_user
    #      ↓
    # Check disabled status
    #      ↓
    # read_users_me()
    #
    # Therefore current_user is already a User object.
    print("current_user:", current_user)

    return current_user


# -------------------------------------------------------------------
# Protected endpoint: User's items
# -------------------------------------------------------------------

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[
        User,
        Depends(get_current_active_user),
    ],
):
    # This endpoint uses the exact same authentication
    # dependency chain as /users/me/.
    #
    # In a real application, current_user.username would
    # be used to query the user's items from the database.

    print(
        "current_user in /users/me/items:",
        current_user,
    )

    return current_user
