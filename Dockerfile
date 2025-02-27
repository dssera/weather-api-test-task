FROM python:3.11-slim

WORKDIR /src

COPY . .

RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]

EXPOSE 80

ENV PYTHONPATH=/src/app

COPY wait-for-it.sh /src/wait-for-it.sh

COPY init_db.py /src/

ENTRYPOINT ["sh", "-c", "/src/wait-for-it.sh db:5432 -- python /src/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 80 --reload"]

