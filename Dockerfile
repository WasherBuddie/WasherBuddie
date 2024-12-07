# Backend Stage
FROM python:3.12-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY . .

# Frontend Stage
FROM node:16-alpine AS frontend

WORKDIR /app

# Copy the entire washerbuddie directory
COPY washerbuddie/ .

# Clear any existing node_modules and build directories
RUN rm -rf node_modules build

# Install dependencies and build
RUN npm install --legacy-peer-deps
RUN npm run build

# Final Stage
FROM python:3.12-slim

WORKDIR /app

# Copy backend files
COPY --from=backend /app /app

# Ensure static directory exists
RUN mkdir -p static

# Copy frontend build to static directory
COPY --from=frontend /app/build/ ./static/

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000
ENV NODE_ENV=production

EXPOSE 10000

# Start the application with gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app