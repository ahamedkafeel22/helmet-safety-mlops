import time
import os
from ultralytics import YOLO
from app.utils import logger

MODEL_PATH = os.getenv("MODEL_PATH", "models/best.pt")
CLASS_NAMES = {0: "head", 1: "helmet", 2: "person"}

# Load model once at startup
logger.info(f"Loading model from {MODEL_PATH}")
model = YOLO(MODEL_PATH)
logger.info("Model loaded successfully")

def run_inference(image_path: str, conf: float = 0.5) -> dict:
    start = time.time()

    results = model(image_path, conf=conf)[0]

    helmet_count = 0
    head_count = 0
    person_count = 0
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        conf_score = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if cls == 0: head_count += 1
        elif cls == 1: helmet_count += 1
        else: person_count += 1

        detections.append({
            "class": CLASS_NAMES[cls],
            "confidence": round(conf_score, 3),
            "bbox": [x1, y1, x2, y2]
        })

    inference_time = round(time.time() - start, 3)
    logger.info(f"Inference complete | time={inference_time}s | helmets={helmet_count} | violations={head_count}")

    return {
        "detections": detections,
        "helmet_count": helmet_count,
        "head_count": head_count,
        "person_count": person_count,
        "inference_time_s": inference_time
    }