from dataapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Cresting the database class
class users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100))
    new_york = db.relationship("new_york", backref = "user_name", lazy = True)

    def __init__(self, name, email,password):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return f"user('{self.name}', '{self.email})"

class new_york(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    company_symbol = db.Column(db.String(100), unique = False, nullable = False)
    open_val = db.Column(db.Integer)
    high_val = db.Column(db.Integer)
    low_val = db.Column(db.Integer)
    close_prediction = db.Column(db.Integer, default = 0)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, company_symbol, open_val, high_val, low_val, prediction, user_id):
        self.company_symbol = company_symbol
        self.open_val = open_val
        self.high_val = high_val
        self.low_val = low_val
        self.close_prediction = prediction
        # self.date_time = datetime.utcnow
        self.user_id = user_id

    def __repr__(self):
        return f"new_york('{self.company_symbol}', '{self.open_val}', '{self.high_val}', '{self.low_val}', '{self.close_prediction}', '{self.date_time}')"