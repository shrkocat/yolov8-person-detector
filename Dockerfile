# ──────────────────────────────────────────────
# YOLOv8 Person Detector — Docker Image
# ──────────────────────────────────────────────
FROM python:3.11-slim

# System deps for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Pre-download the YOLOv8n weights so the container doesn't need internet at runtime
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Expose Flask port
EXPOSE 5000

# Camera device index (override with -e CAMERA_INDEX=1 if needed)
ENV CAMERA_INDEX=0

CMD ["python", "main.py"]
