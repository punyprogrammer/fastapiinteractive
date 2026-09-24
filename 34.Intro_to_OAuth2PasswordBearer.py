from typing_extensions import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

# Extracts the Bearer token from the Authorization header.
# It does NOT authenticate the user or verify the JWT.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return {"token": token}
