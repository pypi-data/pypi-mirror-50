# Define your app’s environment with a Dockerfile so it can be reproduced anywhere.
# Python version
FROM python:3.7-alpine

# Set environment variables

# remove .pyc files from our container which is a good optimization.
ENV PYTHONDONTWRITEBYTECODE 1

# buffer our output so it will look “normal” within Docker for us.
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

# Set work directory
WORKDIR /code

# Copy files
COPY . /code

# Copy Pipfile
#COPY Pipfile /code

# Install dependencies
RUN pip install --upgrade setuptools
RUN python -m pip install -U pip
RUN apk add --no-cache --update python3-dev  gcc build-base
RUN pip install tox
RUN pip install -r requirements.txt



