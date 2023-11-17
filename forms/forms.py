# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PreferencesForm(FlaskForm):
    city = StringField('City: ', validators=[DataRequired()])
    place_type = SelectField('Place Type: ', choices=[
        ('all', 'All'),
        ('restaurants', 'Restaurants'),
        ('attractions', 'Attractions')],
                             default='all', validators=[DataRequired()])
    sorting_option = SelectField('Sorting Option: ', choices=[
        ('rating', 'Rating'),
        ('reviews', 'Popularity')],
                                 default='rating', validators=[DataRequired()])
    num_results = SelectField('Number of Results: ', choices=[
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('25', '25')],
                              default='5', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SaveTripForm(FlaskForm):
    trip_name = StringField('Trip Name:', validators=[DataRequired()])
    trip_notes = StringField('Notes:')
    submit = SubmitField('Save Trip')
