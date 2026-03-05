from fastapi import FastAPI, UploadFile, File
from datetime import datetime
import shutil, os

from app.inference import run_inference
from app.compliance import calculate_compliance
from app.utils import logger

app = FastAPI(
    title="Helmet Safety Detection API",
    description="YOLOv8-powered PPE compliance detection — containerized and deployed on AWS EC2",
    version="1.0"
)

@app.on_event("startup")
def startup():
    logger.info("Helmet Safety Detection API started")

@app.get("/")
def home():
    return {
        "service": "Helmet Safety Detection API",
        "model_version": "v1.0",
        "model": "YOLOv8n",
        "helmet_mAP50": 0.982,
        "status": "running"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"Received image: {file.filename}")
        result = run_inference(temp_path)
        compliance = calculate_compliance(
            result["helmet_count"],
            result["head_count"]
        )

        return {
            "model_version": "v1.0",
            **compliance,
            "person_count": result["person_count"],
            "total_detections": len(result["detections"]),
            "inference_time_s": result["inference_time_s"],
            "detections": result["detections"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True, "version": "v1.0"}