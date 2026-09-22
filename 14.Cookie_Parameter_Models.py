# Cookie Parameter Models
# FastAPI 0.115+ lets you group related cookies
# into a single Pydantic model.

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserPreferences(BaseModel):
    # Default values are used when the cookies are not provided.
    theme: str = "light"
    font_size: int = 14
    language: str = "en"


# Cookie() tells FastAPI to populate the model from cookies.
@app.get("/preferences/")
def get_preferences(
    prefs: UserPreferences = Cookie()
):
    return {
        "preferences": prefs.model_dump()
    }
