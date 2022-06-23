FROM python:3.9.5-slim-buster

# set work directory
WORKDIR .

# # set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get -y install libpq-dev gcc

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .