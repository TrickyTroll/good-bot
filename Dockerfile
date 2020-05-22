#Instruction for building the video automation.

#Sets the base image to python3
FROM python:3

#Sets the working directory for other instructions.
WORKDIR /usr/src/app

#Installs the requirements for the program.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
