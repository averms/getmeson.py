FROM docker.io/library/debian:oldstable-slim
RUN apt-get update -qy \
    && apt-get install -qy python3 ca-certificates
COPY / /root/
