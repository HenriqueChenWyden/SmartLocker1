FROM python:3.11-slim
RUN CMD ["sh", "-c", "python3 -c \"from app.face_service import train_all; train_all()\" && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

RUN mkdir -p /app/dataset
ENV DATASET_DIR=/app/dataset
ENV STORAGE_BACKEND=local

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]