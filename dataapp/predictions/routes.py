from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp import db
from dataapp.predictions.forms import NyseForm, BeersForm
from dataapp.support.regression import nyse_reg, beer_reg
from dataapp.models import new_york, beer_review, users

predict = Blueprint("predict", __name__)


# Trying to create async funcitons
def nyse_predict(vals):
    vals = nyse_reg(vals)
    print(vals)

@predict.route('/nyse', methods=["POST", "GET"])
@login_required
def nyse():
    form = NyseForm()
    if form.validate_on_submit():
        try:
            vals = list([form.company_symbol.data, form.open_val.data, form.high_val.data, form.low_val.data])
            nyse_data = nyse_reg(vals)
            nyse_predict(vals)
            nyse_db = new_york(company_symbol= form.company_symbol.data, open_val= form.open_val.data,
                        high_val= form.high_val.data, low_val = form.low_val.data, prediction=nyse_data[-1], user_id=current_user.id)
            db.session.add(nyse_db)
            print("In the function")
            db.session.commit()
            flash(f'ID: {nyse_db.id} ', 'info')
            flash(f'Successfully predicted. You can also view these predictions in the dashboard', 'success')
            return redirect(url_for("main.dashboard"))
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
            print("Data aaa gaya")
            beer_data = beer_reg(list([form.beer_name.data, form.review_aroma.data, form.review_pallete.data, form.review_taste.data, form.review_appearance.data, form.beer_abv.data]))
            print(beer_data)
            beer_db = beer_review(beer_data[0], beer_data[1], beer_data[2], beer_data[3], beer_data[4], beer_data[5], beer_data[6], user_id=current_user.id)
            db.session.add(beer_db)
            db.session.commit()
            flash(f'ID: {beer_db.id}', 'info')
            flash(f'Successfully predicted. You can also view these predictions in the dashboard', 'success')
            print("Before Loading")
            return redirect(url_for("main.dashboard"))
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

