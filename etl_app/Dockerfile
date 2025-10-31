FROM python:3.11-slim

# System dependencies for psycopg2 and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire etl_app project into /app
COPY . .

# Default command: run main.py
CMD ["python", "main.py"]
