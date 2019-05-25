FROM ubuntu:18.04

# system basics
RUN apt-get update && \
  apt-get -y --no-install-recommends install build-essential python3 python3-dev python3-setuptools python3-pip git && \
  apt-get clean

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt