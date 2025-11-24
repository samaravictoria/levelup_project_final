// src/api.js
const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function detectEmotion(blob) {
  // envia imagem para backend que usa DeepFace
  const fd = new FormData();
  fd.append("file", blob, "capture.jpg");

  const resp = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: fd,
  });

  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error(txt || "Erro ao analisar a imagem");
  }

  const data = await resp.json();
  // Esperamos { quest: { id, title, description, xp, icon } }
  return data;
}
