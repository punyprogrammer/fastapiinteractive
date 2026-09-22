# Header Parameters
# Learn to read and validate HTTP headers

from fastapi import FastAPI,Header
# The Header() tells fastapi to treat it as a header and not query param
# Browser headers have hyphens like 'User-Agent'
# as python vars cannot have hyphens these are converted to "user_agent"
app = FastAPI()
@app.get("/headers/info/")
def get_header_info(
    user_agent:str|None = Header(default=None),
    accept_language:str | None = Header(default='en'),
):
    return {
        "user_agent":user_agent,
        "accept_language":accept_language
    }
@app.get("/secure/data/")
def get_secure_data_header(
    x_token:str =Header(),
    x_request_id:str|None = Header(default=None)
):
    return {
        "data":"secret",
        "token":x_token,
        "request_id":x_request_id
    }
