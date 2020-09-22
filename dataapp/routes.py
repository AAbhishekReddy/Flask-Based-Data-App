from flask import escape, request, render_template, session, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required

from dataapp import app, db, bcrypt
from dataapp.forms import RegistrationForm, LoginForm, NyseForm
from dataapp.support.regression import nyse_reg
from dataapp.models import users, new_york

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title = "Home")


@app.route('/nyse', methods=["POST", "GET"])
@login_required
def nyse():
    form = NyseForm()
    if form.validate_on_submit():
        nyse_data = nyse_reg(list([form.company_symbol.data, form.open_val.data, form.high_val.data, form.low_val.data]))
        nyse_db = new_york(company_symbol= form.company_symbol.data, open_val= form.open_val.data,
                    high_val= form.high_val.data, low_val = form.low_val.data, prediction=nyse_data[-1], user_id=current_user.id)
        db.session.add(nyse_db)
        db.session.commit()
        flash(f'Successfully predicted. You can also view these predictions in the dashboard', 'success')
        
        return render_template("predictions.html", posts = nyse_data)
    return render_template("nyse.html", form = form)

# Beers
@app.route('/beers', methods=["POST", "GET"])
@login_required
def beers():
    return render_template("beers.html", name = None)

# Dashboard Page
@app.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():
    user = users.query.get(current_user.id)
    post = user.new_york
    print(post)
    if not post:
        flash("No predictions done yet.", 'danger')
    return render_template("dashboard.html", post = post)    

# predictions page
@app.route('/predictions')
@login_required
def prediction_page(prediction = None):
    if "user_id" in session and "name" in session:
        return render_template("predictions.html", name = session["name"])    
    return render_template("predictions.html")

# About page
@app.route('/about')
def about():
    if "user_id" in session and "name" in session:
        return render_template("about.html", title = "Home", name = session["name"])
    return render_template("about.html", title = "Home")


# New functions
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = users(form.username.data, form.email.data, hash_pass)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account has been created for {form.username.data} and you can now login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    print("logging Out.")
    logout_user()
    return redirect(url_for('home'))