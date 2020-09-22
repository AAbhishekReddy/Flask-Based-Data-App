from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class NyseForm(FlaskForm):
    myChoices = ["AMZN", "AAPL", "MSFT"]
    company_symbol = SelectField(u'Company Symbol', choices = myChoices, validators = [DataRequired()])
    open_val = IntegerField(u'Opening Value', validators = [DataRequired()])
    high_val = IntegerField(u'Highest Value', validators = [DataRequired()])
    low_val = IntegerField(u'Lowest Value', validators = [DataRequired()])
    submit = SubmitField('PREDICT')