from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

import io


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Plant Disease Detection API",
    description="API for plant disease detection using Vision Transformer",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Plant Disease Detection API",
        "status": "running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "ViT-B/16",
        "model_loaded": False
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check file type
    if not file.content_type.startswith("image/"):

        return {
            "success": False,
            "message": "Please upload a valid image."
        }

    # Read image
    contents = await file.read()

    try:

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

    except Exception:

        return {
            "success": False,
            "message": "Unable to read the uploaded image."
        }

    # --------------------------------------------------------
    # TEMPORARY DEMO PREDICTION
    # --------------------------------------------------------
    #
    # This will later be replaced with:
    #
    # image -> preprocessing -> ViT -> prediction
    #
    # --------------------------------------------------------

    return {
        "success": True,
        "filename": file.filename,
        "disease": "Tomato Early Blight",
        "confidence": 94.7,
        "recommendation": (
            "Remove infected leaves, improve air circulation, "
            "and monitor the plant regularly."
        ),
        "model": "Demo prediction"
    }










# import io
# import json
# from pathlib import Path

# from fastapi import FastAPI, File, HTTPException, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image, UnidentifiedImageError

# # ============================================================
# # SETTINGS
# # ============================================================

# BASE_DIR = Path(__file__).resolve().parent
# CHECKPOINT_PATH = BASE_DIR.parent / "models" / "vit_b16_best.pth"
# CLASSES_PATH = BASE_DIR.parent / "models" / "classes.json"  # list of 38 names, in training order

# MAX_UPLOAD_MB = 5
# ALLOWED_TYPES = {"image/jpeg", "image/png"}
# TOP_K = 3

# DEFAULT_ADVICE = (
#     "Consult a local agronomist to confirm the diagnosis before treating the crop."
# )

# # Fill this in over time: class name -> management advice.
# RECOMMENDATIONS = {
#     "Tomato___Early_blight": (
#         "Remove infected leaves, improve air circulation, "
#         "and monitor the plant regularly."
#     ),
#     "Tomato___healthy": "No disease detected. Keep watering and monitoring regularly.",
# }

# # ============================================================
# # OPTIONAL: LOAD THE TRAINED MODEL
# # ============================================================
# # If the checkpoint and classes.json exist, the API uses the real model.
# # Otherwise it falls back to a clearly marked demo response.

# model = None
# class_names: list[str] = []
# preprocess = None
# torch = None

# try:
#     import torch as _torch
#     import torch.nn as nn
#     from torchvision.models import ViT_B_16_Weights, vit_b_16

#     torch = _torch

#     if CHECKPOINT_PATH.exists() and CLASSES_PATH.exists():
#         class_names = json.loads(CLASSES_PATH.read_text(encoding="utf-8"))

#         net = vit_b_16(weights=None)
#         net.heads.head = nn.Linear(net.heads.head.in_features, len(class_names))

#         # Assumes the checkpoint is a plain state_dict. If you saved a dict such as
#         # {"model_state_dict": ...}, load that key instead.
#         state = torch.load(CHECKPOINT_PATH, map_location="cpu")
#         net.load_state_dict(state)
#         net.eval()

#         model = net
#         # Must match the transforms used during training and validation.
#         preprocess = ViT_B_16_Weights.DEFAULT.transforms()
#         print(f"Loaded model with {len(class_names)} classes.")
#     else:
#         print("Checkpoint or classes.json not found. Running in demo mode.")
# except Exception as exc:  # torch missing, bad checkpoint, etc.
#     model = None
#     print(f"Model not loaded ({exc}). Running in demo mode.")


# # ============================================================
# # FASTAPI APP
# # ============================================================

# app = FastAPI(
#     title="Plant Disease Detection API",
#     description="API for plant disease detection using Vision Transformer",
#     version="1.1.0",
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home():
#     return {"message": "Plant Disease Detection API", "status": "running"}


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy",
#         "model": "ViT-B/16",
#         "model_loaded": model is not None,
#     }


# # ============================================================
# # PREDICTION
# # ============================================================

# def run_model(image: Image.Image) -> list[dict]:
#     """Return the top-K predictions as [{class_name, confidence (%)}, ...]."""
#     tensor = preprocess(image).unsqueeze(0)  # [1, 3, 224, 224]
#     with torch.no_grad():
#         logits = model(tensor)
#         probs = torch.softmax(logits, dim=1)[0]
#     values, indices = torch.topk(probs, k=min(TOP_K, len(class_names)))
#     return [
#         {"class_name": class_names[i], "confidence": round(float(v) * 100, 1)}
#         for v, i in zip(values.tolist(), indices.tolist())
#     ]


# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     if file.content_type not in ALLOWED_TYPES:
#         raise HTTPException(status_code=415, detail="Upload a JPG or PNG image.")

#     contents = await file.read()

#     if len(contents) > MAX_UPLOAD_MB * 1024 * 1024:
#         raise HTTPException(
#             status_code=413, detail=f"Image is larger than {MAX_UPLOAD_MB} MB."
#         )

#     try:
#         image = Image.open(io.BytesIO(contents)).convert("RGB")
#     except (UnidentifiedImageError, OSError):
#         raise HTTPException(status_code=400, detail="Unable to read the uploaded image.")

#     # ---------------- Real model ----------------
#     if model is not None:
#         top = run_model(image)
#         best = top[0]
#         return {
#             "success": True,
#             "demo": False,
#             "filename": file.filename,
#             "class_name": best["class_name"],
#             "confidence": best["confidence"],
#             "top_predictions": top,
#             "recommendation": RECOMMENDATIONS.get(best["class_name"], DEFAULT_ADVICE),
#             "model": "ViT-B/16",
#         }

#     # ---------------- Demo fallback ----------------
#     # Hard-coded placeholder. Not a real prediction.
#     return {
#         "success": True,
#         "demo": True,
#         "filename": file.filename,
#         "class_name": "Tomato___Early_blight",
#         "confidence": 94.7,
#         "top_predictions": [
#             {"class_name": "Tomato___Early_blight", "confidence": 94.7},
#             {"class_name": "Tomato___Late_blight", "confidence": 3.1},
#             {"class_name": "Tomato___healthy", "confidence": 1.0},
#         ],
#         "recommendation": RECOMMENDATIONS["Tomato___Early_blight"],
#         "model": "Demo prediction",
#     }