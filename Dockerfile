FROM python:3.9

WORKDIR /dataproject

COPY . /dataproject

RUN pip install --no-cache-dir -r requirements.txt
