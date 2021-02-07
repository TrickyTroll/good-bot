FROM python:latest
RUN mkdir -pv \
            /video/commands \
            /video/read \
            /video/slides \
            /video/audio \
            /video/recording \
            /video/project
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt