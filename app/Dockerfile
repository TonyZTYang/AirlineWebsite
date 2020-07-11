FROM python:3.8-slim
WORKDIR /app
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt
COPY . .
CMD [ "flask","run" ]