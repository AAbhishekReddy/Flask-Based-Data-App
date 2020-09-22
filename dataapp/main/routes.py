from flask import escape, request, render_template, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp.models import users, new_york, beer_review

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html", title = "Home")

# Dashboard Page
@main.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():
    user = users.query.get(current_user.id)
    nyse = user.new_york
    beers = beer_review.query.filter_by(user_id=current_user.id).all()
    print(beers)
    if not nyse and not beers:
        flash("No predictions done yet.", 'danger')
    return render_template("dashboard.html", post = nyse, beers = beers)    

# About page
@main.route('/about')
def about():
    return render_template("about.html", title = "Home")
