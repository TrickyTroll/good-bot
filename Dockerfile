FROM ubuntu:latest


ADD ./* $HOME/src/


# This is done because npm requires the tzdata package.
RUN apt update; apt upgrade -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.8 pv \
	imagemagick \
	gifsicle \
	pv \
	npm; \
    npm install asciicast2gif
# ADD . /home/app
# The previous add command should be replaced by something else.
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app
COPY . .
RUN pip3 install -r requirements.txt

WORKDIR /tutorial
VOLUME ["/tutorial"]

ENTRYPOINT ["python3", "/home/app/so_it_begins.py"]