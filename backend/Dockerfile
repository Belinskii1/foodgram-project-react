FROM python:3.8-slim
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000
#CMD ["python3", "manage.py", "runserver", "0:8000"]
