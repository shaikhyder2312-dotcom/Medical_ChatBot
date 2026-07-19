FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY setup.py .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]