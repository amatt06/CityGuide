from botocore.exceptions import ClientError
from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms.forms import RegistrationForm, LoginForm, PreferencesForm, SaveTripForm
from API.google_api_controller import GoogleMapsAPIController
from controllers.user_register_controller import register_user
from controllers.user_login_controller import authenticate, logout
from decorators.decorators import login_required, logout_required
from controllers.trip_controller import TripController
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET', 'POST'], endpoint='login')
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if authenticate(form.email.data, form.password.data):
            return redirect(url_for('preferences'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'], endpoint='register')
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        result = register_user(form.email.data, form.password.data)
        if result is None:
            flash("Email already exists.", 'error')
            return render_template('register.html', form=form)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout', endpoint='logout_route')
@login_required
def logout_route():
    logout()
    return redirect(url_for('login'))


@app.route('/preferences', methods=['GET', 'POST'], endpoint='preferences')
@login_required
def preferences():
    form = PreferencesForm()
    save_trip_form = SaveTripForm()
    if form.validate_on_submit():
        city = form.city.data
        place_type = form.place_type.data
        sorting_option = form.sorting_option.data
        num_results = int(form.num_results.data)

        api_controller = GoogleMapsAPIController()
        google_maps_data = api_controller.get_google_maps_data(city, sorting_option, num_results, place_type)

        return render_template('results.html', google_maps_data=google_maps_data, save_trip_form=save_trip_form)

    return render_template('preferences-input.html', form=form)


@app.route('/results', endpoint='results')
@login_required
def results():
    return render_template('results.html')


@app.route('/save_trip', methods=['POST'], endpoint='save_trip')
@login_required
def save_trip():
    try:
        trip_controller = TripController()

        trip_id = trip_controller.generate_trip_id()

        email = session['user_email']
        title = request.form['trip_name']
        trip_data = request.form.to_dict()
        s3_key = trip_controller.save_to_s3(email, trip_id, title, trip_data)

        trip_controller.save_to_dynamodb(trip_id, email, title, request.form['trip_notes'], s3_key)

        print('Trip saved successfully!', 'success')
        return redirect(url_for('trips'))

    except ClientError as e:
        print(f"Error saving trip: {e}", 'error')
        return redirect(url_for('preferences'))


@app.route('/trips', endpoint='trips')
@login_required
def trips():
    return render_template('trips.html')


if __name__ == '__main__':
    app.run()
