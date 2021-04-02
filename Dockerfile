FROM ubuntu:latest

ENV HOME /root
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ENV GOPATH /usr/local/go/bin

RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-pip \
	python3.9 \
	ffmpeg \
	ttyrec \
	wget \
	git

WORKDIR /install

RUN wget https://dl.google.com/go/go1.16.linux-arm64.tar.gz; \
    tar -C /usr/local -xzf go1.16.linux-arm64.tar.gz; \
    export PATH=$PATH:/usr/local/go/bin; \
    go get github.com/sugyan/ttyrec2gif	

RUN mkdir -pv \
            /video/commands \
            /video/read \
            /video/slides \
            /video/audio \
            /video/recording \
            /video/project

RUN pip3 install --upgrade google-cloud-texttospeech

WORKDIR /runner
COPY ./runner /runner/
RUN pip3 install .

WORKDIR /app
COPY ./src /app/
COPY ./requirements.txt /app/
RUN pip3 install -r requirements.txt

WORKDIR /env
COPY .env /env

ENV GOOGLE_APPLICATION_CREDENTIALS="/env/google-tts.json"

WORKDIR $HOME
