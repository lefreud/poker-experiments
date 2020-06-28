FROM ubuntu:focal-20200606

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3.8 \
    python3-pip
RUN apt install -y git
RUN pip3 install black==19.10b0

RUN apt install -y build-essential gdb
RUN apt install -y cmake

# RUN ln -fs /usr/share/zoneinfo/America/Montreal /etc/localtime

