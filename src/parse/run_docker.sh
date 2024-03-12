#!/bin/bash

# Stop and remove any running container of the image nux/parse:latest
docker ps -q --filter ancestor=nux/parse:latest | xargs -r docker stop | xargs -r docker rm

# Remove the Docker image
docker rmi nux/parse:latest

# Build the Docker image
docker build --platform linux/amd64 -t nux/parse:latest .

# Run the Docker container
docker run -p 8001:8001 nux/parse:latest