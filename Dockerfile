# Stage 1 - React build
FROM node:19.5.0-alpine AS react-build

ARG REACT_APP_PASSWORD
ARG REACT_APP_SPOTIFY_CLIENT_ID
ARG REACT_APP_SPOTIFY_CLIENT_SECRET
ARG REACT_APP_SPOTIFY_REDIRECT_URI
ARG REACT_APP_USERNAME
ARG REACT_APP_BASE_URL

ENV REACT_APP_PASSWORD=$REACT_APP_PASSWORD
ENV REACT_APP_SPOTIFY_CLIENT_ID=$REACT_APP_SPOTIFY_CLIENT_ID
ENV REACT_APP_SPOTIFY_CLIENT_SECRET=$REACT_APP_SPOTIFY_CLIENT_SECRET
ENV REACT_APP_SPOTIFY_REDIRECT_URI=$REACT_APP_SPOTIFY_REDIRECT_URI
ENV REACT_APP_USERNAME=$REACT_APP_USERNAME
ENV REACT_APP_BASE_URL=$REACT_APP_BASE_URL

WORKDIR /tmp
COPY ./client/ /tmp/
RUN npm ci
RUN npm run build --mode production

# Stage 2 - Python requirements
FROM python:3.10-slim AS requirements-stage
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
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    libfontconfig1 \
    libice6 \
    libsm6 \
    libxext6 \
    libxrender1 \
    tesseract-ocr \
    tesseract-ocr-eng \
    *libarchive13*
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY --from=requirements-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=react-build /tmp/build/ /app/client/build
CMD exec gunicorn -k uvicorn.workers.UvicornWorker main:app