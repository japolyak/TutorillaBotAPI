FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT