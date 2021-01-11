FROM ubuntu:latest

RUN apt update; apt upgrade -y

RUN apt install -y \
	python3-dev \
	python3-pip \
	python3.9 \
	ttyrec \
	wget \
    curl \
    vim \
    zsh \
	git \
	pv 

RUN yes Y | sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime \
    sh ~/.vim_runtime/install_awesome_vimrc.sh \
    git clone https://github.com/junegunn/seoul256.vim.git ~/.vim_runtime/my_plugins/seoul256.vim
	
RUN wget https://dl.google.com/go/go1.15.linux-arm64.tar.gz; \
    tar -C /usr/local -xzf go1.15.linux-arm64.tar.gz; \
	export PATH=$PATH:/usr/local/go/bin; \
	source ~/.profile; \
	go get github.com/sugyan/ttyrec2gif 

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

#ENTRYPOINT [ "zsh" ]

