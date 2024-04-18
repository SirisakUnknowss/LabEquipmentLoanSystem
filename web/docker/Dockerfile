# pull official base image
FROM python:3.9.4-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# RUN python -m pip install pip
RUN python -m ensurepip --upgrade \
    && python -m pip install --upgrade setuptools \
    && apt update && apt-get upgrade -y
# Install Pillow dependencies
RUN apt install libxml2-dev libxslt-dev libffi-dev gcc curl
RUN apt install tk-dev tcl-dev
# install psycopg2 dependencies
RUN apt install gcc

WORKDIR /usr/src/app/
COPY ./docker/requirements.txt ./docker/requirements.txt

RUN pip install -r ./docker/requirements.txt

COPY . .