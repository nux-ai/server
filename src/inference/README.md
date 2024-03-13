uvicorn main:app --reload --host 8003

## Docker Commands:

docker build --platform linux/amd64 -t nux-ai/parse:latest .

docker run -p 8001:8001 nux-ai/parse:latest