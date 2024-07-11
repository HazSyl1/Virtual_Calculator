FROM python:3.9-slim 

WORKDIR /
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libopencv-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]