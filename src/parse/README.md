## Docker Commands:

docker build --platform linux/amd64 -t nux/parse:latest .

docker run -p 8001:8001 nux/parse:latest

## Run without docker:

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8001


