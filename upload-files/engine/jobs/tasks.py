from celery import Celery


app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@app.task(name="tasks.process_file")
def read_file(file_path: str):
    with open(file_path, "r") as f:
        data = f.read()
    return f"reading file {file_path} and size {len(data)}"
