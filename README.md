<div align="center">

# YOLOv8 Person Detector

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-111F68?style=for-the-badge&logo=ultralytics&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-111F68?style=for-the-badge&logo=ultralytics&logoColor=white)

</div>

---


A real-time person detection app using your webcam and a pretrained YOLOv8 model. It runs a local web server and streams your camera feed — live — with bounding boxes drawn around every detected person.

Built with Python, Flask, OpenCV, and Ultralytics YOLOv8.

---

## Project Structure

```
yolov8-person-detector/
│
├── app/
│   ├── __init__.py          # Makes app a Python package (leave empty)
│   ├── detector.py          # YOLOv8 inference and bounding box logic
│   └── camera.py            # Webcam capture and MJPEG stream generator
│
├── static/
│   └── index.html           # Browser UI for viewing the live stream
│
├── main.py                  # Flask server entry point
├── requirements.txt         # Python dependencies
└── Dockerfile               # Docker container configuration
```

---

## System Requirements

| Requirement | Minimum |
|---|---|
| OS | Windows 10/11, macOS 11+, Ubuntu 20.04+ |
| Python | 3.9 or higher |
| RAM | 4 GB (8 GB recommended) |
| Webcam | Any USB or built-in webcam |
| Internet | Required on first run (downloads YOLOv8 weights ~6 MB) |
| GPU | Optional — runs on CPU, GPU speeds it up significantly |

---

## How to Run (Local — Recommended)

### Step 1 — Make sure Python is installed
```bash
python --version
# Should show 3.9 or higher
```

### Step 2 — Navigate to the project folder
```bash
cd yolov8-person-detector
```

### Step 3 — Create a virtual environment
```bash
python -m venv venv
```

### Step 4 — Activate the virtual environment

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
```
> If you get a permissions error, run PowerShell as Administrator and run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

You'll know it worked when you see `(venv)` at the start of your terminal line.

### Step 5 — Install dependencies
```bash
pip install -r requirements.txt
```
> This may take a few minutes the first time.

### Step 6 — Run the app
```bash
python main.py
```

### Step 7 — Open your browser
```
http://localhost:5000
```

Your webcam will turn on and you'll see the live feed with green bounding boxes drawn around detected people.

---

## How to Run with Docker

> **Note:** Docker cannot directly access your webcam on Windows or macOS. Use the local method above for those systems. Docker works best on Linux.

### Build the image
```bash
docker build -t yolov8-detector .
```

### Run the container (Linux)
```bash
docker run --device=/dev/video0 -p 5000:5000 yolov8-detector
```

### Use a different camera index
```bash
docker run --device=/dev/video1 -e CAMERA_INDEX=1 -p 5000:5000 yolov8-detector
```

---

## 🔧 Configuration

| Setting | Where to change | Default |
|---|---|---|
| YOLOv8 model size | `app/detector.py` — change `yolov8n.pt` | `yolov8n` (nano) |
| Detection confidence threshold | `app/detector.py` — change `0.4` | `0.4` (40%) |
| Camera index | `main.py` or env var `CAMERA_INDEX` | `0` |
| Stream resolution | `app/camera.py` — `CAP_PROP_FRAME_WIDTH/HEIGHT` | `1280x720` |

### Model size options (trade speed for accuracy)

| Model | File | Speed | Accuracy |
|---|---|---|---|
| Nano | `yolov8n.pt` | Fastest | Lower |
| Small | `yolov8s.pt` | Fast | Good |
| Medium | `yolov8m.pt` | Moderate | Better |
| Large | `yolov8l.pt` | Slow | High |
| XLarge | `yolov8x.pt` | Slowest | Highest |

---

## Dependencies

| Package | Purpose |
|---|---|
| `ultralytics` | YOLOv8 model loading and inference |
| `flask` | Local web server and video stream endpoint |
| `opencv-python-headless` | Webcam capture and frame processing |
| `torch` + `torchvision` | Deep learning backend for YOLOv8 |
| `numpy` | Array processing |

---

## Troubleshooting

**Camera not opening**
- Make sure no other app (Zoom, Teams, etc.) is using your webcam
- Try changing `CAMERA_INDEX` to `1` if you have multiple cameras

**Slow detection / low FPS**
- Switch to `yolov8n.pt` (nano) in `detector.py` for the fastest speed
- Lower the stream resolution in `camera.py`

**`venv\Scripts\activate` permission error on Windows**
- Run PowerShell as Administrator
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Module not found errors**
- Make sure your virtual environment is activated (you should see `(venv)` in the terminal)
- Re-run: `pip install -r requirements.txt`

---

## Notes

- On first launch, YOLOv8 automatically downloads the model weights file. An internet connection is required.
- The Flask development server warning (`Do not use in production`) is normal and safe to ignore for local use.
- Only the `person` class (COCO class ID 0) is detected. The model can detect 80 object classes in total — edit `detector.py` to add more.
