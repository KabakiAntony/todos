FROM python:3.7.17-alpine3.17

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=wsgi.py

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]