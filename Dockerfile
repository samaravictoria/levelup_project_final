FROM python:3.10-slim

# =======================
# DEPENDÊNCIAS DO SISTEMA
# =======================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libopenblas-dev \
    liblapack-dev \
    libjpeg62-turbo-dev \
    && rm -rf /var/lib/apt/lists/*

# =======================
# WORKDIR
# =======================
WORKDIR /app

# =======================
# INSTALAR DEPENDÊNCIAS PYTHON
# =======================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =======================
# COPIAR CÓDIGO
# =======================
COPY . .

# =======================
# CONFIGURAÇÃO
# =======================
ENV PORT=8000 \
    TASKS_API=http://tasks-service:8001/api/tasks \
    PYTHONUNBUFFERED=1

# =======================
# START SERVER
# =======================
CMD ["gunicorn", "app:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "200"]
