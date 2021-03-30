FROM python:3.7.6
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY . /app
CMD gunicorn --bind 0.0.0.0:$PORT app:app