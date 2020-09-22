from flask import escape, request, render_template, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required

from dataapp.models import users, new_york

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
    post = user.new_york
    if not post:
        flash("No predictions done yet.", 'danger')
    return render_template("dashboard.html", post = post)    

# About page
@main.route('/about')
def about():
    return render_template("about.html", title = "Home")
