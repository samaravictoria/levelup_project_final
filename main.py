# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
from PIL import Image
import numpy as np
import httpx
import io
import uuid
import json
import os

JAVA_API_URL = os.environ.get("JAVA_API_URL", "http://localhost:8080/tasks")

app = FastAPI(title="LevelUp AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMOTION_MAP = {
    "happy":   {"title": "Aura Alegre", "description": "Energia positiva detectada.", "xp": 100, "icon": "😄"},
    "sad":     {"title": "Sombrio Determinado", "description": "Indicador emocional baixo.", "xp": 60, "icon": "😢"},
    "neutral": {"title": "Equilíbrio Mental", "description": "Expressão estável detectada.", "xp": 80, "icon": "😐"},
    "angry":   {"title": "Fúria Controlada", "description": "Intensidade elevada identificada.", "xp": 120, "icon": "😠"},
    "surprise":{"title": "Revelação", "description": "Variação inesperada detectada.", "xp": 90, "icon": "😲"},
    "fear":    {"title": "Coragem Interior", "description": "Sinal de receio percebido.", "xp": 110, "icon": "😨"},
    "disgust": {"title": "Força Interior", "description": "Reação negativa detectada.", "xp": 70, "icon": "🤢"},
}

def build_task(emotion: str):
    base = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"])
    return {
        "id": str(uuid.uuid4()),
        "team_id": None,
        "assigned_by": "AI Engine",
        "title": base["title"],
        "description": base["description"],
        "type": "emotion",
        "xp": base["xp"],
        "due_in_minutes": 1440,
        "metadata": json.dumps({
            "icon": base["icon"],
            "detected_emotion": emotion
        })
    }


# ---------------------------------------------------------
# 🔥 DeepFace seguro (nunca quebra)
# ---------------------------------------------------------
def safe_analyze_emotion(image_pil):
    try:
        result = DeepFace.analyze(
            img_path=image_pil,             # ← CORREÇÃO AQUI (não usar numpy)
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv",      # ← CORREÇÃO AQUI
            prog_bar=False
        )

        if isinstance(result, list):
            result = result[0]

        return result.get("dominant_emotion", "neutral")

    except Exception as e:
        print("⚠️ DeepFace falhou:", e)
        return "neutral"


# ---------------------------------------------------------
# 📌 ENDPOINT PRINCIPAL
# ---------------------------------------------------------
@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except:
            print("⚠️ ERRO ao abrir imagem — fallback")
            emotion = "neutral"
            return {"status": "ok", "detected_emotion": emotion, "task": build_task(emotion)}

        # Reduz a imagem se for grande
        max_width = 640
        w, h = image.size
        if w > max_width:
            nh = int(max_width * h / w)
            image = image.resize((max_width, nh))

        # --------------------------------------------------
        # 🧠 Analisa emoção de forma segura
        # --------------------------------------------------
        emotion = safe_analyze_emotion(image)

        task_payload = build_task(emotion)

        # --------------------------------------------------
        # 📡 Envia task ao backend Java
        # --------------------------------------------------
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                r = await client.post(JAVA_API_URL, json=task_payload)
                if r.status_code >= 500:
                    print("⚠️ Java retornou erro")
        except Exception as e:
            print("⚠️ Falha ao enviar para Java:", e)

        return {
            "status": "ok",
            "detected_emotion": emotion,
            "task": task_payload
        }

    except Exception as error:
        print("🔥 ERRO GERAL:", error)
        return {
            "status": "ok",
            "detected_emotion": "neutral",
            "task": build_task("neutral"),
            "fallback": True
        }
