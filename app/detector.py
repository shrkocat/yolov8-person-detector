from ultralytics import YOLO
import cv2

# Load the pretrained YOLOv8 model (downloads automatically on first run)
model = YOLO("yolov8n.pt")  # 'n' = nano (fastest). Options: yolov8s, yolov8m, yolov8l, yolov8x

PERSON_CLASS_ID = 0  # COCO class index for "person"


def detect_persons(frame):
    """
    Run YOLOv8 inference on a single frame.
    Returns the annotated frame with bounding boxes drawn only around persons.
    """
    results = model(frame, verbose=False)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id == PERSON_CLASS_ID and conf > 0.4:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"Person {conf:.0%}"

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 100), 2)

            # Draw label background
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), (0, 255, 100), -1)

            # Draw label text
            cv2.putText(frame, label, (x1 + 3, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

    # Person count overlay
    count = sum(1 for b in results.boxes if int(b.cls[0]) == PERSON_CLASS_ID and float(b.conf[0]) > 0.4)
    cv2.putText(frame, f"People: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 2, cv2.LINE_AA)

    return frame
