FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    ffmpeg \
    libsm6 \
    libxext6 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python3", "app.py"]
