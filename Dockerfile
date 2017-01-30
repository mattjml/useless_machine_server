FROM python:3.6-alpine

MAINTAINER mattjmlane@gmail.com

# Ordered like this (before "ADD . /root/"), python3 dependency
# installation can be cached and so *so* much quicker
ADD requirements.txt /
RUN pip install -r requirements.txt

ADD . /root/
WORKDIR /root/

CMD FLASK_APP=api.py flask run --host=0.0.0.0
