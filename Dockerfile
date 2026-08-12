FROM ubuntu:22.04

RUN apt-get update && apt-get install -y nano && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

COPY  config/ /site_config/

CMD ["python3", "site_config/main.py"]

VOLUME ["config", "/site_config"]