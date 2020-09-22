from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp import db
from dataapp.predictions.forms import NyseForm
from dataapp.support.regression import nyse_reg
from dataapp.models import new_york

predict = Blueprint("predict", __name__)

@predict.route('/nyse', methods=["POST", "GET"])
@login_required
def nyse():
    form = NyseForm()
    print("In the function")
    if form.validate_on_submit():
        print("Validated")

        nyse_data = nyse_reg(list([form.company_symbol.data, form.open_val.data, form.high_val.data, form.low_val.data]))
        nyse_db = new_york(company_symbol= form.company_symbol.data, open_val= form.open_val.data,
                    high_val= form.high_val.data, low_val = form.low_val.data, prediction=nyse_data[-1], user_id=current_user.id)
        db.session.add(nyse_db)
        db.session.commit()
        flash(f'Successfully predicted. You can also view these predictions in the dashboard', 'success')
        return render_template("predictions.html", posts = nyse_data)
    return render_template("nyse.html", form = form)

# Beers
@predict.route('/beers', methods=["POST", "GET"])
@login_required
def beers():
    return render_template("beers.html", name = None)

# predictions page
@predict.route('/predictions')
@login_required
def prediction_page(prediction = None):
    if "user_id" in session and "name" in session:
        return render_template("predictions.html", name = session["name"])    
    return render_template("predictions.html")

