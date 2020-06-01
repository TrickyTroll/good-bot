FROM ubuntu:latest


ADD ./* $HOME/src/

RUN apt update; apt upgrade -y

RUN apt update; apt upgrade -y; \
	apt install -y \
	python3-dev \
	python3-pip \
	python3.8 pv \
	imagemagick \
	gifsicle \
	npm ; \
	npm install --global asciicast2gif

# ADD . /home/app
# The previous add command should be replaced by something else.
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app
COPY . .
RUN pip3 install -r requirements.txt

WORKDIR /tutorial
VOLUME ["/tutorial"]

ENTRYPOINT ["/home/app/so_it_begins.py"]