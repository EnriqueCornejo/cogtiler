FROM python:3.6
MAINTAINER Vizzuality Science Team info@vizzuality.com

ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
RUN apt-get update && apt-get install -yq \
    libgdal-dev \
    ca-certificates \
    && apt-get clean

WORKDIR /cog

COPY main.py main.py

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh entrypoint.sh

EXPOSE 6767
COPY ./cog cog

ENTRYPOINT ["./entrypoint.sh"]