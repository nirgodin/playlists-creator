FROM python:3.10-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    ffmpeg \
    libxext6 \
    tesseract-ocr \
    tesseract-ocr-eng \
    *libarchive13*
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn -k uvicorn.workers.UvicornWorker main:app