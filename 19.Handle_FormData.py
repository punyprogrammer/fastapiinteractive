# Form Data
#
# - Form data sends key-value pairs in the request body, commonly using
#   application/x-www-form-urlencoded.
# - Sample form data:
#   username=amar&password=secret123
#
# - JSON uses application/json and sends structured objects such as:
#   {"username": "amar", "password": "secret123"}
#
# - In FastAPI, JSON is typically handled with Pydantic models,
#   while form fields use Form().
#
# - OAuth2 token endpoints commonly use form-encoded parameters
#   such as username and password.
#
# - FastAPI provides OAuth2PasswordRequestForm to parse these
#   OAuth2 form fields.
#
# - After authentication, the server typically returns the access
#   token as JSON.
#
# - multipart/form-data is mainly used when sending files with form fields.


# Sample form-data view:
#
# Content-Type: application/x-www-form-urlencoded
#
# ┌────────────┬──────────────┐
# │ Key        │ Value        │
# ├────────────┼──────────────┤
# │ username   │ amar         │
# │ password   │ secret123    │
# └────────────┴──────────────┘
#
# Encoded request body:
# username=amar&password=secret123


from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
def handle_login(
    username: str = Form(),
    password: str = Form(),
):
    return {
        "username": username
    }
