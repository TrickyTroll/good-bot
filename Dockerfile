FROM ubuntu:latest


ADD ./* $HOME/src/


# This is done because npm requires the tzdata package.
RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.8 \
	ttyrec \
	wget \
	pv \
	git
	
RUN mkdir /home/all
WORKDIR /home/all

RUN wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz; \
    tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz; \
	export PATH=$PATH:/usr/local/go/bin; \
	source ~/.profile; \
	go get github.com/sugyan/ttyrec2gif
	
# ADD . /home/app
# The previous add command should be replaced by something else.
COPY requirements.txt /home/all
COPY . .
#RUN cat requirements.txt | xargs -n 1 -L 1 pip3 install
WORKDIR /tutorial
VOLUME ["/tutorial"]

ENTRYPOINT ["python3", "/home/all/so_it_begins.py"]
