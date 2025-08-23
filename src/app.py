from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from scan import scan_document as scan_module  # Import the scan function
import os
import uuid
from pathlib import Path

app = FastAPI(title="Document Scanner API", version="1.0.0")

# Create necessary directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "saved_images"
STATIC_DIR = "src/static"

for directory in [UPLOAD_DIR, OUTPUT_DIR, STATIC_DIR]:
    os.makedirs(directory, exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main HTML page"""
    return FileResponse("src/static/index.html")

@app.post("/scan")
async def scan_document(file: UploadFile = File(...)):
    """
    Upload and scan a document image using the existing scan.py module
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
    
    # Save uploaded file
    upload_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
    
    try:
        # Save the uploaded file
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Use the imported scan module instead of subprocess
        try:
            scanned_path = scan_module(upload_path, OUTPUT_DIR)
        except Exception as scan_error:
            raise HTTPException(status_code=500, detail=f"Scanning failed: {str(scan_error)}")
        
        if not os.path.exists(scanned_path):
            raise HTTPException(status_code=500, detail="Scanned image not found")
        
        # Clean up the uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        # Return the scanned image for download
        def iter_file():
            with open(scanned_path, 'rb') as file_like:
                yield from file_like
        
        response = StreamingResponse(
            iter_file(),
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=scanned_document.png"
            }
        )
        
        # Optional: Clean up scanned file after serving
        # Note: In production, implement proper cleanup strategy
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up files in case of error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Document Scanner API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)