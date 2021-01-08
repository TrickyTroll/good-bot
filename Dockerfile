FROM ubuntu:latest

RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.9 \
	ttyrec \
	wget \
    curl \
    zsh \
	git \
	pv 

RUN yes Y | sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
	
RUN wget https://dl.google.com/go/go1.13.linux-arm64.tar.gz; \
    tar -C /usr/local -xzf go1.13.linux-arm64.tar.gz; \
	export PATH=$PATH:/usr/local/go/bin; \
	source ~/.profile; \
	go get github.com/sugyan/ttyrec2gif 

COPY . $HOME/src/
WORKDIR /tutorial
VOLUME ["/tutorial"]

ENTRYPOINT [ "zsh" ]
