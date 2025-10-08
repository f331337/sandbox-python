import os
from typing import Annotated, Union

from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI()


UPLOAD_DIRECTORY = "uploads"  # folder where you want to store files

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        contents = await file.read()
        with open(file_location, "wb") as f:
            f.write(contents)

        return {"filename": file.filename, "saved_to": file_location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        await file.close()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
