# Backend Stage: Use Python 3.12 slim image for the Flask backend
FROM python:3.12-slim AS backend

# Set working directory for backend (Flask)
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application files into the container
COPY . /app/

# Set up Flask environment variables (optional)
ENV FLASK_APP=/app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Frontend Stage: Use Node.js 16-alpine for the React frontend
FROM node:16-alpine AS frontend

# Set working directory for frontend (React)
WORKDIR /app/washerbuddie

# Copy package.json and install React dependencies
COPY washerbuddie/package.json .
RUN npm install

# Copy the rest of the React app files into the container
COPY washerbuddie/ .

# Build the React application
RUN npm run build

# Final Stage: Combine Backend and Frontend
FROM python:3.12-slim

# Set working directory for the combined application
WORKDIR /app

# Copy backend and frontend files from their respective stages
COPY --from=backend /app /app
COPY --from=frontend /app/washerbuddie/build /app/washerbuddie/build

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose ports for Flask (5000)
EXPOSE 5000

# Set the command to run the Flask server (React is static content in this setup)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
