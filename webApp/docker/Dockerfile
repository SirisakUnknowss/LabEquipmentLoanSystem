# pull official base image
FROM python:3.9.4-buster

# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN python -m pip install pip
RUN python -m pip install --upgrade setuptools
RUN apt update && apt-get upgrade -y
# Install Pillow dependencies
RUN apt install libxml2-dev libxslt-dev libffi-dev gcc curl
RUN apt install tk-dev tcl-dev
# install psycopg2 dependencies
RUN apt install gcc

COPY . .

RUN pip install -r ./docker/requirements.txt