FROM python:3.6-slim

MAINTAINER mattjmlane@gmail.com

ADD . /root/
WORKDIR /root/

RUN pip install -r requirements.txt

CMD FLASK_APP=api.py flask run --host=0.0.0.0
