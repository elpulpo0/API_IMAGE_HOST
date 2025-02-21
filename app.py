from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import shutil
from fastapi.staticfiles import StaticFiles


app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "url": f"/uploads/{file.filename}"}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
