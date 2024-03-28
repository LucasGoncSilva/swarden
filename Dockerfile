FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY SWARDEN/requirements.txt /code/

RUN pip install -r requirements.txt

COPY /SWARDEN /code/
