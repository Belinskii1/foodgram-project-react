FROM python:3.8-slim
WORKDIR /code 
COPY . .
RUN pip install -r requirements.txt 
CMD exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
