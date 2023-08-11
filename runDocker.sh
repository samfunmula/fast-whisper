docker build -t fast-whisper .
docker run -it --rm --runtime=nvidia -p 8000:8000 -e USE_SINGLE_GPU='true' fast-whisper
