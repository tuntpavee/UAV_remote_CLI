from fastapi import FastAPI, UploadFile, File
import shutil
import os
import time

app = FastAPI()
UPLOAD_DIR = "received_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.perf_counter()
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Read and write the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    # Calculate file size in MB
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    # Calculate speed (MB/s)
    speed = file_size_mb / duration if duration > 0 else 0

    return {
        "filename": file.filename,
        "size_mb": round(file_size_mb, 2),
        "duration_seconds": round(duration, 4),
        "speed_mb_s": round(speed, 2),
        "status": "success"
    }

# Run: uvicorn main:app --host 0.0.0.0 --port 8000
