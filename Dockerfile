# Stage 1 - cv2 requirements
FROM ubuntu
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

# Stage 2 - python requirements
FROM python:3.10-slim as requirements-stage
WORKDIR /tmp
RUN pip install poetry==1.6.1
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 3 - build
FROM python:3.10-slim
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
COPY --from=requirements-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn -k uvicorn.workers.UvicornWorker main:app