# File Uploads
#
# FastAPI provides two main ways to handle file uploads:
#
# 1. File()
#    - Receives the entire file as bytes.
#    - The file content is loaded into memory.
#    - Simple to use.
#    - Best suited for smaller files.
#
# 2. UploadFile
#    - Provides a file-like object.
#    - Includes file metadata such as filename and content type.
#    - Supports file operations and streaming.
#    - More memory efficient for larger files.
#
# Why have two approaches?
#
# File() → Simple + entire file available as bytes
# UploadFile → Metadata + file-like interface + better for large files


from fastapi import FastAPI, File, UploadFile

app = FastAPI()


# File() receives the entire uploaded file as bytes.
# Useful when you need to directly process the file contents.
@app.post("/files/")
def post_files(file: bytes = File()):
    return {
        "file_size": len(file)
    }


# UploadFile provides a file-like object and metadata.
# Better suited for larger files and file-processing workflows.
@app.post("/uploadfile/")
def upload_files(file: UploadFile):
    return {
        "filename": file.filename
    }
