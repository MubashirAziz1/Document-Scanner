from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from scan import scan_document as scan_module
import os

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("saved_images", exist_ok=True)
os.makedirs("src/static", exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("src/static/index.html")

@app.post("/scan")
async def scan_document(file: UploadFile = File(...)):
    # Save uploaded file
    upload_path = f"uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Scan document
    scanned_path = scan_module(upload_path, "saved_images")

    def iter_file():
        with open(scanned_path, 'rb') as file_like:
            yield from file_like
    
    return StreamingResponse(iter_file(), media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)