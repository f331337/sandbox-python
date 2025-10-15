import os

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from jobs.tasks import read_file
from jobs.tasks import app as celery_app

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIRECTORY = "uploads"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}
    elif task_result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": "failure",
            "error": str(task_result.result),
        }
    elif task_result.state == "SUCCESS":
        return {"task_id": task_id, "status": "success", "result": task_result.result}
    else:
        return {"task_id": task_id, "status": task_result.state}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    contents = await file.read()
    with open(file_location, "wb") as f:
        f.write(contents)

    task = read_file.delay(file_location)

    return {"filename": file.filename, "task_id": task.id}

    # try:
    #     contents = await file.read()
    #     with open(file_location, "wb") as f:
    #         f.write(contents)
    #
    #     return {"filename": file.filename, "saved_to": file_location}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    # finally:
    #     await file.close()
