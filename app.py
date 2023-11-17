from flask import Flask, render_template, redirect, url_for, request
from forms.forms import RegistrationForm, LoginForm, PreferencesForm, SaveTripForm
from API.google_api_controller import GoogleMapsAPIController
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('preferences'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Backend Implementation here;
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/preferences', methods=['GET', 'POST'])
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


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/save_trip', methods=['POST'])
def save_trip():
    # Handle the saving logic here
    # Example: Save the trip_name in the database

    trip_name = request.form['trip_name']
    trip_notes = request.form['trip_notes']
    # Save trip_name to the database (you need to implement this logic)

    # After saving, redirect to the trips page
    return redirect(url_for('trips'))


@app.route('/trips')
def trips():
    return render_template('trips.html')


if __name__ == '__main__':
    app.run()
