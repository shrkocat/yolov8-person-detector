import cv2
from app.detector import detect_persons


def generate_frames(camera_index: int = 0):
    """
    Generator that captures frames from the webcam,
    runs YOLOv8 person detection, and yields MJPEG bytes.
    """
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera at index {camera_index}")

    # Optional: set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Run detection
            annotated = detect_persons(frame)

            # Encode as JPEG
            ret, buffer = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue

            # Yield as multipart MJPEG stream
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )
    finally:
        cap.release()
