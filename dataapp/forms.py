from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from dataapp.models import users


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        new_user = users.query.filter_by(name = username.data).first()

        if new_user:
            raise ValidationError("The username is already taken.")

    def validate_email(self, email):
        new_user = users.query.filter_by(email = email.data).first()

        if new_user:
            raise ValidationError("This Email has already been registered, Please try to login.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class NyseForm(FlaskForm):
    myChoices = ["AMZN", "AAPL", "MSFT"]
    company_symbol = SelectField(u'Company Symbol', choices = myChoices, validators = [DataRequired()])
    open_val = IntegerField(u'Opening Value', validators = [DataRequired()])
    high_val = IntegerField(u'Highest Value', validators = [DataRequired()])
    low_val = IntegerField(u'Lowest Value', validators = [DataRequired()])
    submit = SubmitField('PREDICT')