# Flask-Based-Data-App
This is a simple web app that is an imitation to an app cretaed on streamlit. You can check out the previous app's source code [here](https://github.com/AAbhishekReddy/data-app).

## Introduction
This app is a basic web app that has been built using FLASK. It enables the user to run prediction on logistic regression models. 

## Packages Used
1. Flask
    + Flask-SQLAlchemy
    + Flask-Login
    + Flask-bcrypt
    + Flask-wtforms
    + Flask-restplus
2. Celery
3. Numpy and Pickle

[RabbitMQ](https://www.rabbitmq.com/) has been used as a messaging broker to handle the queues for Celery. 