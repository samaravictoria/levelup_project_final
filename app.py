# app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timedelta
import io
import numpy as np
import cv2
from deepface import DeepFace
import uuid

DATABASE_URL = "sqlite:///./levelup.db"  # trocar para postgres em produção
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    xp = Column(Integer, default=0)

class Quest(Base):
    __tablename__ = "quests"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    xp = Column(Integer, default=10)
    type = Column(String)  # 'wellness' | 'social' | 'work'
    created_at = Column(DateTime, default=datetime.utcnow)
    auto_generated = Column(Boolean, default=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    user = relationship("User")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LevelUp Emotion-Driven Quests")

# Helper: convert uploaded image bytes -> cv2 image
def bytes_to_cv2(img_bytes: bytes):
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Não foi possível decodificar a imagem")
    return img

# Mapping emotion -> quests (configurável)
def generate_quest_from_emotion(dominant_emotion: str, user_id: str | None):
    # Map básico; ajuste/expanda conforme UX
    emotion = dominant_emotion.lower()
    if emotion in ("angry", "fear", "disgust", "sad"):
        # prioriza wellness + check-in
        return {
            "title": "Pausa Relax — Respirar 5 minutos",
            "description": "Você parece tenso(a). Faça 5 minutos de respiração guiada (4-4-4). Volte com calma.",
            "xp": 15,
            "type": "wellness",
        }
    if emotion in ("surprise", "neutral"):
        return {
            "title": "Pausa Curta — Alongamento",
            "description": "Faça 3 minutos de alongamento para aliviar a postura.",
            "xp": 10,
            "type": "wellness",
        }
    if emotion in ("happy", "joy"):
        # aproveita o bom momento: social ou produtividade leve
        return {
            "title": "Compartilhe algo bom",
            "description": "Compartilhe um pequeno sucesso do dia no canal do time (1-2 frases).",
            "xp": 12,
            "type": "social",
        }
    # Padrão
    return {
        "title": "Pausa Mindful",
        "description": "Tire 3 minutos para respirar e anotar como está se sentindo.",
        "xp": 10,
        "type": "wellness",
    }

@app.post("/analyze")
async def analyze(user_id: str = Form(None), file: UploadFile = File(...)):
    # recebe imagem, analisa emoção e gera quest
    contents = await file.read()
    try:
        img = bytes_to_cv2(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Imagem inválida: {e}")

    # DeepFace analyze - usar detector 'mtcnn' ou 'opencv' conforme ambiente
    try:
        # working with ndarray; DeepFace accepts file path or ndarray
        result = DeepFace.analyze(img_path = img, actions = ['emotion'], enforce_detection=False)
        dominant_emotion = result.get("dominant_emotion") or "neutral"
    except Exception as e:
        # fallback - quando ouver erro, assume neutral
        dominant_emotion = "neutral"

    # gerar quest
    quest_data = generate_quest_from_emotion(dominant_emotion, user_id)

    # salvar no DB
    db = SessionLocal()
    quest = Quest(
        title=quest_data["title"],
        description=quest_data["description"],
        xp=quest_data["xp"],
        type=quest_data["type"],
        user_id=user_id
    )
    db.add(quest)
    db.commit()
    db.refresh(quest)

    # resposta
    return JSONResponse({
        "quest": {
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "xp": quest.xp,
            "type": quest.type
        },
        "detected_emotion": dominant_emotion
    })
