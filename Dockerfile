FROM ubuntu:latest


ADD ./* $HOME/src/


# This is done because npm requires the tzdata package.
RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.8 \
	pv
	
# ADD . /home/app
# The previous add command should be replaced by something else.
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app
COPY . .
RUN cat requirements.txt | xargs -n 1 -L 1 pip3 install
WORKDIR /tutorial
VOLUME ["/tutorial"]

#ENTRYPOINT ["python3", "/home/app/so_it_begins.py"]