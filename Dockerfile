FROM ubuntu:20.04


ADD ./* $HOME/src/

RUN apt update; apt upgrade -y

RUN apt install -y python3-dev build-essential libssl-dev libffi-dev python python3-pip python3.8 vim 

ADD . /home/tutorial
# The previous add command should be replaced by something else.
WORKDIR /home/tutorial
RUN pip3 install -r requirements.txt

COPY . . 

#RUN chmod +x ./app/app.py
#CMD /home/myapp/app/app.py
