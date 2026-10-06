FROM python:3.10-bookworm

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/dicomutils
WORKDIR /tmp/dicomutils
RUN pip install .

WORKDIR /opt