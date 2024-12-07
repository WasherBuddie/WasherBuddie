# Backend Stage
FROM python:3.12-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY requirements.txt .
COPY app.py .
COPY wsgi.py .
COPY conftest.py .
COPY setup.py .
COPY pyproject.toml .
COPY render.yaml .
COPY docker-compose.yml .

# Copy directories
COPY src/ ./src/
COPY mongoDB/ ./mongoDB/
COPY Tests/ ./Tests/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Frontend Stage
FROM node:16-alpine AS frontend

WORKDIR /app

# Copy package files
COPY washerbuddie/package*.json ./

# Clean install dependencies
RUN npm cache clean --force && \
    npm install --legacy-peer-deps && \
    npm install ajv ajv-keywords

# Copy the rest of the frontend application
COPY washerbuddie/public ./public
COPY washerbuddie/src ./src

# Set environment variables for build
ENV NODE_ENV=production
ENV CI=true

# Build the React application
RUN npm run build

# Final Stage
FROM python:3.12-slim

WORKDIR /app

# Install necessary system packages and gunicorn
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && pip install gunicorn && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY --from=backend /app /app

# Create static directory
RUN mkdir -p static

# Copy frontend build files to static directory
COPY --from=frontend /app/build/ ./static/

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000
ENV NODE_ENV=production

EXPOSE 10000

# Start with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "1", "--threads", "8", "--timeout", "0", "app:app"]