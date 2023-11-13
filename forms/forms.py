# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
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

    location_type = SelectField('Location Type: ', choices=[
        ('restaurants', 'Restaurants'),
        ('attractions', 'Attractions'),
        ('both', 'Both')],
                               default='attractions', validators=[DataRequired()])

    pricing = SelectField('Pricing: ', choices=[
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('both', 'Both')],
                         default='free', validators=[DataRequired()])

    sorting_option = SelectField('Sorting Option: ', choices=[
        ('rating', 'Rating'),
        ('popularity', 'Popularity')],
                                 default='rating', validators=[DataRequired()])

    submit = SubmitField('Submit')
