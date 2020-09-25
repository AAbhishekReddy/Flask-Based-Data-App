from flask import Blueprint, flash
from flask_login import current_user, login_required
from time import sleep


from dataapp.backend_tasks.celery_make import make_celery
from dataapp import app, db
from dataapp.models import new_york, beer_review, users
from dataapp.support.regression import nyse_reg, beer_reg

celery = make_celery(app)

@celery.task()
def nyse_db_add(data):
    data = nyse_reg(data)
    nyse_db = new_york(company_symbol= data[0], open_val= data[1],
                high_val= data[2], low_val = data[3], prediction=data[5], user_id=data[4])
    sleep(10)
    db.session.add(nyse_db)
    db.session.commit()
    return "Data added to NYSE database."

@celery.task()
def beers_db_add(beer_data):
    beer_data = beer_reg(beer_data)
    beer_db = beer_review(beer_data[0], beer_data[1], beer_data[2], beer_data[3], beer_data[4], beer_data[5], beer_data[7], user_id=beer_data[6])
    sleep(10)
    db.session.add(beer_db)
    db.session.commit()
    return "Data added to Beers database."
