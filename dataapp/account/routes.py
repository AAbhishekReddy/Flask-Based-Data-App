from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import login_user, logout_user

from dataapp import db, bcrypt
from dataapp.account.forms import RegistrationForm, LoginForm
from dataapp.models import users

account = Blueprint("account", __name__)

# New functions
@account.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = users(form.username.data, form.email.data, hash_pass)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account has been created for {form.username.data} and you can now login!', 'success')
        return redirect(url_for('account.login'))
    return render_template('register.html', title='Register', form=form)


@account.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Login Successful! Welcome.", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@account.route("/logout")
def logout():
    print("logging Out.")
    logout_user()
    return redirect(url_for('main.home'))