FROM python:3.9-slim

RUN apt-get update
RUN apt-get -y install wget
RUN apt-get -y install gzip

RUN pip install pandas
RUN pip install sqlalchemy
RUN pip install psycopg2-binary

WORKDIR /app 

COPY insert_data.py insert_data.py

ENTRYPOINT [ "python", "insert_data.py" ]
