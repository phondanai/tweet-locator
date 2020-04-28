FROM python:3.6

ENV PYTHONUNBUFFERED=1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--worker-class" ,"eventlet","-w","1","application:app","--bind","0.0.0.0"]
