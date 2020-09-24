from flask_login import login_user, logout_user, current_user

from dataapp import bcrypt, db
from dataapp.support.regression import nyse_reg, beer_reg
from dataapp.models import users, new_york, beer_review

def account(username, email, password):
    if current_user:
        logout_user()
    user = users.query.filter_by(email=email).first()
    flag = 0
    if user:
        if user and bcrypt.check_password_hash(user.password, password):
            flag = 1

    if flag == 0:
        hash_pass = bcrypt.generate_password_hash(password).decode("utf-8")
        user = users(username, email, hash_pass)
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    print(current_user)


# Handling nyse data
def nyse_data_add(data):
    account(data["username"], data["email"], data["password"])
    nyse_list = list([data["company_symbol"], data["open_val"], data["high_val"], data["low_val"]])
    nyse_list = nyse_reg(nyse_list)
    nyse_db = new_york(company_symbol= data["company_symbol"], open_val= data["open_val"],
                        high_val= data["high_val"], low_val = data["low_val"], prediction = nyse_list[-1], user_id=current_user.id)
    db.session.add(nyse_db)
    db.session.commit()
    data["prediction"] = nyse_list[-1]
    return data

def nyse_get():
    if current_user:
        user = users.query.get(current_user.id)
        nyse = user.new_york
        return nyse
    else:
        return {"message" : "No user logged in or no predictions done."}

# handling Beers data
def beer_data_add(data):
    account(data["username"], data["email"], data["password"])
    beer_list = list([data["beer_name"], data["review_aroma"], data["review_pallete"], data["review_taste"], data["review_appearance"], data["beer_abv"]])
    beer_list = beer_reg(beer_list)
    beer_db = beer_review(data["beer_name"], data["review_aroma"], data["review_pallete"], data["review_taste"], data["review_appearance"], data["beer_abv"], beer_list[-1], user_id=current_user.id)
    db.session.add(beer_db)
    db.session.commit()
    data["prediction"] = beer_list[-1]
    return data

def beers_get():
    if current_user:
        print(current_user)
        beers = beer_review.query.filter_by(user_id=current_user.id).all()
        return beers
    else:
        return {"message" : "No user logged in or no predictions done."}