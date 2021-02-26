FROM python:latest

RUN pip install asciinema

RUN mkdir -pv \
            /video/commands \
            /video/read \
            /video/slides \
            /video/audio \
            /video/recording \
            /video/project

WORKDIR /runner
COPY ./runner /runner/
RUN pip install .

WORKDIR /app
COPY ./src /app/
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt