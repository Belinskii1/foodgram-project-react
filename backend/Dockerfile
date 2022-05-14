FROM python:3.8-slim
WORKDIR /code 
COPY . .
RUN pip install -r requirements.txt 
CMD [ "gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
