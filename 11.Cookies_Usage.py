# Cookie Parameters
# Learn to read and validate HTTP cookies in FastAPI.

from fastapi import Cookie, FastAPI

app = FastAPI()


# Required cookie: must be present in the request.
# Optional cookies use defaults when they are missing.
@app.get("/user/settings/")
def read_user_settings(
    session_id: str = Cookie(),
    theme: str | None = Cookie(default="light"),
    language: str | None = Cookie(default="en"),
):
    return {
        "session_id": session_id,
        "theme": theme,
        "language": language,
    }


@app.get("/session/info/")
def read_session_info(
    session_id: str = Cookie(),
):
    return {
        "session_id": session_id,
        "valid": True,
    }


# -------------------------------------------------------------------
# THEORY
# -------------------------------------------------------------------

# Cookies are small pieces of data stored by the browser and sent
# back to the server with subsequent requests.
#
# Common uses:
# - Session management
# - User preferences
# - Tracking
#
# Server → Browser:
# Set-Cookie: session_id=abc123; Path=/; HttpOnly
#
# Browser → Server:
# Cookie: session_id=abc123; theme=dark; language=en


# -------------------------------------------------------------------
# FASTAPI'S COOKIE CLASS
# -------------------------------------------------------------------

# Cookie() works similarly to Query() and Path(), but reads the
# value from the HTTP Cookie header.
#
# Without Cookie(), FastAPI treats session_id as a query parameter.
#
# Example:
#
# session_id: str = Cookie()
#
# Request:
# Cookie: session_id=abc123


# -------------------------------------------------------------------
# REQUIRED VS OPTIONAL COOKIES
# -------------------------------------------------------------------

# Required: no default value.
# Missing cookie → 422 validation error.
#
# session_id: str = Cookie()
#
#
# Optional: has a default value.
#
# theme: str = Cookie(default="light")
#
# Missing theme → "light"
#
#
# Optional with None:
#
# tracking_id: str | None = Cookie(default=None)
#
# Missing tracking_id → None


# -------------------------------------------------------------------
# TYPE CONVERSION
# -------------------------------------------------------------------

# FastAPI converts cookie values to the declared Python type.
#
# font_size: int = Cookie(default=14)
# Cookie value "14" → Python int 14
#
# notifications: bool = Cookie(default=True)
# Cookie value "true" → Python bool True
#
# Invalid values → 422 validation error.


# -------------------------------------------------------------------
# COOKIE vs QUERY vs PATH
# -------------------------------------------------------------------

# Query() → URL query string
# /items?session_id=abc123
#
# Path() → URL path
# /users/abc123
#
# Cookie() → HTTP Cookie header
# Cookie: session_id=abc123


# -------------------------------------------------------------------
# PRACTICAL EXAMPLE
# -------------------------------------------------------------------

# @app.get("/user/settings/")
# def get_user_settings(
#     session_id: str = Cookie(),
#     theme: str = Cookie(default="light"),
#     language: str = Cookie(default="en"),
# ):
#     return {
#         "session_id": session_id,
#         "theme": theme,
#         "language": language,
#     }
#
# Request:
#
# Cookie: session_id=abc123; theme=dark; language=en
#
# Response:
#
# {
#     "session_id": "abc123",
#     "theme": "dark",
#     "language": "en"
# }
