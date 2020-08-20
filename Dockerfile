FROM python:3.8

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD gunicorn -w 4 -b 0.0.0.0:5000 main:app