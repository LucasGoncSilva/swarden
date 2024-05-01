FROM python:latest

WORKDIR /code

COPY SWARDEN/requirements.txt /code/

RUN pip install -r requirements.txt

COPY /SWARDEN /code/
