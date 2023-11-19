from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms.forms import RegistrationForm, LoginForm, PreferencesForm, SaveTripForm
from API.google_api_controller import GoogleMapsAPIController
from controllers.user_register_controller import register_user
from controllers.user_login_controller import authenticate, logout
from decorators.decorators import login_required, logout_required
from controllers.trip_controller import generate_trip_id, save_trip_to_db, save_to_s3
from db.trip_table import get_user_trips, get_trip_details
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
    if request.method == 'POST':
        trip_name = request.form.get('trip_name')
        trip_notes = request.form.get('trip_notes')

        google_maps_data = session.get('google_maps_data', [])

        user_email = session.get('user_email')
        trip_id = generate_trip_id(user_email, trip_name)

        s3_url = save_to_s3(user_email, trip_id, google_maps_data)

        save_trip_to_db(user_email, trip_id, trip_name, trip_notes, s3_url)

        session.pop('google_maps_data', None)

        return redirect(url_for('trips'))

    print("Failed to save trip. Please try again.", 'error')
    return redirect(url_for('preferences'))


@app.route('/trips', endpoint='trips')
@login_required
def trips():
    user_email = session.get('user_email')

    trips_data = get_user_trips(user_email)

    return render_template('trips.html', trips_data=trips_data)


@app.route('/view_trip/<trip_id>', methods=['GET'], endpoint='view_trip')
@login_required
def view_trip(trip_id):
    user_email = session.get('user_email')

    print("Received trip_id:", trip_id)
    trip_details = get_trip_details(user_email, trip_id)
    print("Trip details:", trip_details)
    return render_template('view_trip.html', trip_details=trip_details)


if __name__ == '__main__':
    app.run()
