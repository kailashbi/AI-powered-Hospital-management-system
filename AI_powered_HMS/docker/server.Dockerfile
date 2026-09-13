FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL client and ML binaries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 --retries 10 --no-cache-dir -r requirements.txt

COPY . .

# Note: Pre-trained ML models (.pkl) in ml/models/ are copied above via 'COPY . .'


ENV PORT=5000
ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "server.run:app"]
