from flask import escape, request, render_template, session, url_for, redirect, flash, Blueprint
from flask_login import current_user, login_required
from flask_restplus import Api, Resource, fields
from functools import wraps

from dataapp.api.utils import nyse_data_add, nyse_get, beer_data_add, beers_get

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Username'
    }
}


api = Api(api_blueprint, doc='/doc', authorizations = authorizations, version='1.0', title='Data API',
    description='API linked to the DATA APP')



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'Username' in request.headers:
            token = request.headers['Username']

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if token != 'lmn':
            return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401

        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)

    return decorated




nyse_data = api.model('New york', {"username" : fields.String('username'), "email" : fields.String('email'), "password" : fields.String('password'),
                     'company_symbol' : fields.String('AMZN'), "open_val" : fields.Integer(100),
                     "high_val" : fields.Integer(100), "low_val" : fields.Integer(100)}) 
beers_data = api.model('Beers', {"username" : fields.String('username'), "email" : fields.String('email'), "password" : fields.String('password'),
                     'beer_name' : fields.String('British Empire'), "review_aroma" : fields.Integer("0"),
                     "review_pallete" : fields.Integer("0"), "review_taste" : fields.Integer("0"),
                     "review_appearance" : fields.Integer("0"), "beer_abv" : fields.Integer("0")})

nyse_show = api.model('New york All predictions', {'company_symbol' : fields.String('AMZN'), "open_val" : fields.Integer(100),
                     "high_val" : fields.Integer(100), "low_val" : fields.Integer(100), "close_prediction" : fields.Integer(100)}) 
beers_show = api.model('Beers All predictions', {'beer_name' : fields.String('British Empire'), "review_aroma" : fields.Integer("0"),
                     "review_pallete" : fields.Integer("0"), "review_taste" : fields.Integer("0"),
                     "review_appearance" : fields.Integer("0"), "beer_abv" : fields.Integer("0"), "prediction_review" : fields.Integer("0")})
 


@api.route('/nyse')
class nyse(Resource):

    @api.marshal_with(nyse_show, envelope='NYSE DATA')
    @api.doc(security='apikey')
    @token_required
    def get(self):
        data = nyse_get()
        return data

    @api.expect(nyse_data)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        predictions = nyse_data_add(api.payload)
        return {"close_val (predicted)" : predictions["prediction"]}


@api.route('/beers')
class beers(Resource):

    @api.marshal_with(beers_show, envelope='Beer_data')
    @api.doc(security='apikey')
    @token_required
    def get(self):
        data = beers_get()
        print(data)
        return data

    @api.expect(beers_data)
    @api.doc(security='apikey')
    @token_required
    def post(self):
        predictions = beer_data_add(api.payload)
        return {"Overall review (predicted)" : predictions['prediction'] }
