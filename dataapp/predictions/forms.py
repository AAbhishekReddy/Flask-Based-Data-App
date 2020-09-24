from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange

class NyseForm(FlaskForm):
    myChoices = ["AMZN", "AAPL", "MSFT"]
    company_symbol = SelectField(u'Company Symbol', choices = myChoices, validators = [DataRequired()])
    open_val = IntegerField(u'Opening Value', validators = [DataRequired()])
    high_val = IntegerField(u'Highest Value', validators = [DataRequired()])
    low_val = IntegerField(u'Lowest Value', validators = [DataRequired()])
    submit = SubmitField('PREDICT')

class BeersForm(FlaskForm):
    beer_name = StringField('Beer Name',
                           validators=[DataRequired(), Length(min=2, max=20)], description="Enter the Beer Name")
    review_aroma = IntegerField(u'Aroma Review', validators = [DataRequired(), NumberRange(min = 0, max = 5)])
    review_pallete = IntegerField(u'Pallete Review', validators = [DataRequired(), NumberRange(min = 0, max = 5)])
    review_taste = IntegerField(u'Taste Review', validators = [DataRequired(), NumberRange(min = 0, max = 5)])
    review_appearance = IntegerField(u'Appearenvce Review', validators = [DataRequired(), NumberRange(min = 0, max = 5)])
    beer_abv = IntegerField(u'Beer ABV', validators = [DataRequired(), NumberRange(min = 0, max = 100)])
    submit = SubmitField('PREDICT')