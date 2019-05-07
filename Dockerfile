FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
# To avoid .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
# Note: --no-cache means don't install the registry index on our
# dockerfile. To minimize size of docker contained.

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# Note: Temporarily build dependencies (.tmp-build-deps) is to
# install dependencies for completing the installation and later
# on they are removed. Again to minimize size of the container.
RUN pip install -r /requirements.txt

# Here's where we remove the tmp-build dependencies.
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
RUN adduser -D user
# Note: -D means user created for running applications inside Docker only
USER user