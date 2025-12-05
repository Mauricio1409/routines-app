FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Instalar dependencias necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
