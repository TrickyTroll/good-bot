FROM ubuntu:latest

ENV HOME /root
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	libgtkextra-dev \
	libgconf2-dev \
	libxtst-dev \
	python3-pip \
	libasound2 \
	x11-common \
	libgtk-3.0 \
    asciinema \
	python3.9 \
	libnss3 \
	libxss1 \
	ffmpeg \
	ttyrec \
	unzip \
	sudo \
	wget \
    npm \
	git \
    && rm -rf /var/lib/apt/lists/*

# Install utf8 locale
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

WORKDIR /install
RUN wget https://github.com/TrickyTroll/good-bot-runner/archive/refs/tags/v1.1.0.zip \
	&& unzip v1.1.0.zip
WORKDIR  /install/good-bot-runner-1.1.0
RUN pip3 install .

WORKDIR /app
COPY . /app/
RUN pip install /app/

WORKDIR /install
RUN npm install terminalizer

ENTRYPOINT [ "good-bot" ]

