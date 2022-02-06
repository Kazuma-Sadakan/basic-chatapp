FROM python:3
USER root

COPY requirements.txt .
COPY main.py /root

RUN apt-get update  
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt 

# CMD ["python", "/root/main.py"]