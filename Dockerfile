FROM python:3.8
EXPOSE 5000
WORKDIR /app

# # install supervisord
# RUN apt-get update && apt-get install -y supervisor 

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
# RUN apt-get install python-psycopg2 libpq-dev python-dev -y
COPY . /app

# needs to be set else Celery gives an error (because docker runs commands inside container as root)
ENV C_FORCE_ROOT=1

# CMD ["python", "run.py"]

# run supervisord
# CMD ["/usr/bin/supervisord"]
