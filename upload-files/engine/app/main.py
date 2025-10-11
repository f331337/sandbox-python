import os

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIRECTORY = "uploads"

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
