FROM python:3.12-slim

RUN apt-get update && apt-get install -y nano
RUN apt-get install -y python3 && apt-get install -y python3-pip
RUN pip3 install flask

COPY app/ ./site/

EXPOSE 5000

CMD ["python3", "site/app.py"]

VOLUME ["app", "/site_app"]