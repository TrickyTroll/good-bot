FROM ubuntu


ADD ./* $HOME/src/

RUN apt update; apt upgrade -y

RUN apt install -y python3-dev python3-pip python3.8 

ADD . /home/tutorial
# The previous add command should be replaced by something else.
WORKDIR /home/tutorial
RUN pip3 install -r requirements.txt

COPY . . 

#CMD ["python3", "/home/tutorial/so_it_begins.py"]
