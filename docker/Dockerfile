FROM python:3.6-alpine3.8 AS base
COPY . /home/python/project
RUN apk add --no-cache zip make bash && \
    adduser -D python && \
    chown -R python.python ./home/python && \
    pip install --no-cache-dir -e /home/python/project[test] && \
    pip install --no-cache-dir twine
WORKDIR /home/python/project
USER python
