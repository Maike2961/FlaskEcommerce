FROM python:3.11-slim

WORKDIR /app

EXPOSE 5000

RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY  . /app/

CMD [ "sh", "-c", "python run.py 0.0.0.0:5000"]
