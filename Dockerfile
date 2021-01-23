FROM python:latest
RUN mkdir -pv \
            ~/commands \
            ~/read \
            ~/slides 
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt