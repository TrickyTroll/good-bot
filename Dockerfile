FROM ubuntu:latest

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.9 \
	golang-go \
	ttyrec \
	wget \
	pv \
	git
	
RUN mkdir /home/all
WORKDIR /home/all

RUN export PATH=$PATH:/usr/local/go/bin
RUN /bin/bash -c "source ~/.profile"
RUN /bin/bash -c "go get github.com/sugyan/ttyrec2gif"	

	
RUN mkdir -pv \
            /video/commands \
            /video/read \
            /video/slides \
            /video/audio \
            /video/recording \
            /video/project

WORKDIR /runner
COPY ./runner /runner/
RUN pip3 install .

WORKDIR /app
COPY ./src /app/
COPY ./requirements.txt /app/
RUN pip3 install -r requirements.txt