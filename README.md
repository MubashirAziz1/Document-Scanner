# Document Scanner

A smart document scanner built with OpenCV and FastAPI that automatically detects document edges and transforms images into clean, scanned-like documents. This project uses computer vision techniques to convert photos of documents into high-quality scanned images.

## Features

- **Automatic Edge Detection**: Automatically finds document edges in photos
- **Perspective Transformation**: Corrects perspective and creates a top-down view of documents
- **Image Enhancement**: Converts images to black and white with proper thresholding for a scanned look
- **Web Interface**: Easy-to-use web interface for uploading and scanning documents
- **REST API**: Simple API endpoint for programmatic access
- **Docker Support**: Easy deployment with Docker

## How It Works

1. Upload an image of a document
2. The system detects the document edges using edge detection
3. Applies perspective transformation to get a top-down view
4. Converts the image to grayscale and applies thresholding
5. Returns a clean, scanned-looking document image

## Requirements

- Python 3.11 or higher
- Docker (optional, for containerized deployment)

## Installation

### Method 1: Using Python (Local Setup)

1. **Clone or download this project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t document-scanner .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name document-scanner document-scanner
   ```

## Usage

### Running the Server

#### Using Python directly:
```bash
python -m uvicorn src.app:app --reload
```

Or:
```bash
uvicorn src.app:app --reload
```

#### Using Docker:
If you've already built and started the container, the server should be running. If not:
```bash
docker start document-scanner
```

### Accessing the Application

Once the server is running, open your web browser and go to:
- **Web Interface**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative API Docs**: `http://localhost:8000/redoc`

### Using the Web Interface

1. Open `http://localhost:8000` in your browser
2. Upload an image file containing a document
3. The system will process the image and return a scanned version

### Using the API

#### Scan a Document

**Endpoint**: `POST /scan`

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: File upload (image file)

**Example using curl**:
```bash
curl -X POST "http://localhost:8000/scan" -F "file=@path/to/your/image.jpg"
```

**Example using Python**:
```python
import requests

url = "http://localhost:8000/scan"
with open("document.jpg", "rb") as f:
    response = requests.post(url, files={"file": f})
    
# Save the scanned image
with open("scanned_document.png", "wb") as f:
    f.write(response.content)
```

**Response**:
- Content-Type: image/png
- Body: The scanned document image as PNG

### Using the Command Line

You can also use the scanner directly from the command line:

```bash
python -m src.scan -i path/to/your/image.jpg
```

The scanned image will be saved in the `saved_images` directory.

## Project Structure

```
Document Scanner/
├── src/
│   ├── app.py          # FastAPI application
│   ├── scan.py         # Document scanning logic
│   ├── transform.py    # Perspective transformation functions
│   └── static/
│       └── index.html  # Web interface
├── uploads/            # Temporary storage for uploaded files
├── saved_images/       # Output directory for scanned images
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
└── README.md          # This file
```

## API Endpoints

### GET `/`
Returns the web interface HTML page.

### POST `/scan`
Upload and scan a document image.

**Parameters**:
- `file` (required): Image file to scan

**Returns**: Scanned document image (PNG format)

## Docker Commands

### Build the image:
```bash
docker build -t document-scanner .
```

### Run the container:
```bash
docker run -d -p 8000:8000 --name document-scanner document-scanner
```

### Stop the container:
```bash
docker stop document-scanner
```

### Start the container again:
```bash
docker start document-scanner
```

### Remove the container:
```bash
docker rm -f document-scanner
```

### View container logs:
```bash
docker logs document-scanner
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **OpenCV**: Computer vision library for image processing
- **NumPy**: Numerical computing library
- **scikit-image**: Image processing algorithms
- **imutils**: Convenience functions for OpenCV
- **Pillow**: Python imaging library

## Tips for Best Results

1. **Good Lighting**: Ensure the document is well-lit when taking the photo
2. **Clear Background**: Place the document on a contrasting background
3. **Sharp Focus**: Make sure the image is in focus
4. **Full Document Visible**: Ensure the entire document is visible in the image
5. **Minimal Shadows**: Try to avoid shadows on the document

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, you can change it:
```bash
uvicorn src.app:app --port 8001
```

Or with Docker:
```bash
docker run -d -p 8001:8000 --name document-scanner document-scanner
```

### Module Not Found Error
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Docker Container Not Starting
Check the container logs:
```bash
docker logs document-scanner
```

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Support

If you encounter any problems or have questions, please open an issue in the project repository.

