FROM python:3.8
EXPOSE 5000
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "run.py"]