FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt -y install python3 python3-pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src .

RUN chmod 600 /app/audio

EXPOSE 8000

CMD python3 api.py