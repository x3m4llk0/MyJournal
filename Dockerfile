FROM python:3.10

RUN mkdir /myjournal

WORKDIR /myjournal

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

