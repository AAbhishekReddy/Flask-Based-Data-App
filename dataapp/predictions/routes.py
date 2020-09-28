from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp import db, nyse_stats, beer_stats
from dataapp.predictions.forms import NyseForm, BeersForm
from dataapp.support.regression import nyse_reg, beer_reg
from dataapp.models import new_york, beer_review, users
from dataapp.backend_tasks.tasks import nyse_db_add, beers_db_add

predict = Blueprint("predict", __name__)

@predict.route('/nyse', methods=["POST", "GET"])
@login_required
def nyse():
    form = NyseForm()
    if form.validate_on_submit():
        try:
            vals = list([form.company_symbol.data, form.open_val.data, form.high_val.data, form.low_val.data, current_user.id])
            job = nyse_db_add.delay(vals)
            nyse_stats.append(job)
            flash(f'Job Id: {job.task_id}', 'info')
            flash(f'Job submitted successfully. The predictions will be updated in the Dashboard once complete.', 'success')
            return redirect(url_for("main.home"))
        except Exception as e:
            flash(e, 'danger')
    return render_template("nyse.html", form = form)

# Beers
@predict.route('/beers', methods=["POST", "GET"])
@login_required
def beers():
    form = BeersForm()
    if form.validate_on_submit():
        try:
            beer_data = list([form.beer_name.data, form.review_aroma.data, form.review_pallete.data, form.review_taste.data, form.review_appearance.data, form.beer_abv.data, current_user.id])
            job = beers_db_add.delay(beer_data)
            beer_stats.append(job)
            flash(f'Job Id: {job.task_id}', 'info')
            flash(f'Job submitted successfully. The predictions will be updated in the Dashboard once complete.', 'success')
            return redirect(url_for("main.home"))
        except Exception as e:
            flash(e, 'danger')
    return render_template("beers.html", form = form)

@predict.route('/tasks')
@login_required
def tasks_page():
    status = []
    for job in nyse_stats:
        print(job.status)
    print()
    for job in beer_stats:
        print(job.status)
    print(nyse_stats, beer_stats)
    return render_template("tasks.html", nyse_stats = nyse_stats, beer_stats = beer_stats)