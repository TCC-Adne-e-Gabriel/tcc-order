FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app

WORKDIR /app/

ENV PYTHONPATH=/app

COPY app/ ./app/
COPY scripts/ ./scripts/
COPY .env .env

CMD ["fastapi", "run", "--host", "0.0.0.0","app/main.py"]