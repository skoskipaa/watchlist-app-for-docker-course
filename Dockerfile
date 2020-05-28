FROM python:3.5
WORKDIR /app
RUN apt-get update && apt-get install -y sqlite3
COPY ../ .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./run.py
