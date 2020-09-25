from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp import db
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
            nyse_db_add.delay(vals)
            flash(f'Job submitted successfully. The predictions will be updated in the Dashboard once complete.', 'info')
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
            # beer_data = beer_reg()
            # beer_data.append(current_user.id)
            beers_db_add.delay(beer_data)
            flash(f'Job submitted successfully. The predictions will be updated in the Dashboard once complete.', 'info')
            return redirect(url_for("main.home"))
        except Exception as e:
            flash(e, 'danger')
        # beer = beer_review()
    return render_template("beers.html", form = form)

# predictions page
@predict.route('/predictions')
@login_required
def prediction_page(prediction = None):
    if "user_id" in session and "name" in session:
        return render_template("predictions.html", name = session["name"])    
    return render_template("predictions.html")

