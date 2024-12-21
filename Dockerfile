FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && pip install -r requirements.txt \
    && apt-get remove -y build-essential python3-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "main.py"]