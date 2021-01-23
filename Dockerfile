FROM golang:latest
WORKDIR /app
COPY . /app/
RUN go install github.com/TrickyTroll/good-bot

