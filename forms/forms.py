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

    sorting_option = SelectField('Sorting Option: ', choices=[
        ('rating', 'Rating'),
        ('popularity', 'Popularity')],
                                 default='rating', validators=[DataRequired()])

    submit = SubmitField('Submit')
