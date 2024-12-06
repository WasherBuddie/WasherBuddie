# Backend Stage
FROM python:3.12-slim AS backend

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY app.py .
COPY conftest.py .
COPY render.yaml .
COPY docker-compose.yml .

# Frontend Stage
FROM node:16-alpine AS frontend

# Set working directory
WORKDIR /app

# Copy the entire washerbuddie directory
COPY washerbuddie/ ./

# Install dependencies from the correct location
RUN npm install

# Build the React application
RUN npm run build

# Final Stage
FROM python:3.12-slim

WORKDIR /app

# Copy backend files
COPY --from=backend /app /app

# Copy frontend build to a directory Flask can serve
COPY --from=frontend /app/build ./static

# Install Python dependencies again in final stage
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]