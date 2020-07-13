FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git curl
COPY requirement.txt requirement.txt
RUN pip install -Ur requirement.txt