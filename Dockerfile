FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements.txt requirements.txt

RUN pip install numpy==1.14.3
RUN pip install -r requirements.txt
RUN pip install --no-deps pandas==0.23.0
RUN pip install gunicorn

ADD . /app

RUN python src/make_data.py

ENV NAME World

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]