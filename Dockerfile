#Dockerfile to containerize this script
FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

COPY dynamic-ip-change-detector.py dynamic-ip-change-detector.py

RUN pip3 install -r requirements.txt

CMD [ "python3", "dynamic-ip-change-detector.py"]