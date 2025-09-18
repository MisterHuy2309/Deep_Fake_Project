from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torchvision import transforms
import cv2
import numpy as np
import tempfile
import os

# ------------------ Cấu hình ------------------
DEVICE = "cpu"
MODEL_PATH = "D:/Desktop/Deep_fake/backend/models/deepfake_resnet18_full.pth"
IMG_SIZE = (224, 224)
FRAME_INTERVAL = 30  # dự đoán 1 frame / 30 frames

# ------------------ Load model ------------------
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()
print("✅ Model loaded successfully on CPU!")

# ------------------ Transform ảnh ------------------
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # chuẩn ImageNet
                         std=[0.229, 0.224, 0.225])
])

# ------------------ Hàm dự đoán ảnh ------------------
def predict_image_array(img_array):
    img_tensor = transform(img_array).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = model(img_tensor)
        probs = F.softmax(output, dim=1).cpu().numpy()[0]

    print("Raw logits:", output.cpu().numpy())  # debug
    print("Probabilities:", probs)              # debug

    pred = int(np.argmax(probs))
    label = "Real" if pred == 0 else "Fake"
    score = round(float(probs[pred]) * 100, 2)  # %
    return label, score

# ------------------ Hàm dự đoán video ------------------
def predict_video_file(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None

    frame_count = 0
    real_scores = []
    fake_scores = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % FRAME_INTERVAL == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_tensor = transform(frame_rgb).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                output = model(frame_tensor)
                probs = F.softmax(output, dim=1).cpu().numpy()[0]

            print(f"Frame {frame_count} - Raw logits:", output.cpu().numpy())  # debug
            print(f"Frame {frame_count} - Probabilities:", probs)              # debug

            real_scores.append(probs[0])
            fake_scores.append(probs[1])

        frame_count += 1

    cap.release()

    if len(real_scores) == 0 and len(fake_scores) == 0:
        return None, None

    avg_real = np.mean(real_scores) if real_scores else 0
    avg_fake = np.mean(fake_scores) if fake_scores else 0

    if avg_real >= avg_fake:
        label = "Real"
        score = round(avg_real * 100, 2)
    else:
        label = "Fake"
        score = round(avg_fake * 100, 2)

    return label, score

# ------------------ FastAPI app ------------------
app = FastAPI(title="DeepFake Detector")

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cho Vue/React gọi API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Endpoint dự đoán ảnh ------------------
@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            return JSONResponse(content={"status": "error", "message": "Cannot read image"}, status_code=400)

        label, score = predict_image_array(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return {"status": "success", "result": label, "score": float(score)}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# ------------------ Endpoint dự đoán video ------------------
@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        label, score = predict_video_file(tmp_path)
        os.remove(tmp_path)

        if label is None:
            return JSONResponse(content={"status": "error", "message": "Cannot open video"}, status_code=400)

        return {"status": "success", "result": label, "score": float(score)}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
