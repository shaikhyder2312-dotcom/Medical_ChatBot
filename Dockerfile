FROM python:3.10-slim

WORKDIR /app

# Prevent Python from creating .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependencies first for better Docker layer caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 8080

CMD ["python", "app.py"]