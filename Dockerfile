FROM ubuntu:latest

ENV HOME /root
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	python3-pip \
    asciinema \
    asciinema \
	python3.9 \
	ffmpeg \
	ttyrec \
	wget \
	git \
    && rm -rf /var/lib/apt/lists/*

# Install utf8 locale
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

WORKDIR /install

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

WORKDIR /project
VOLUME ["/project"]

ENTRYPOINT ["python3", "/app/cli.py"]
