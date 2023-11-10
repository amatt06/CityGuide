from flask import Flask, render_template, redirect, url_for
from forms.forms import RegistrationForm, LoginForm
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
    return render_template('login.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences-input.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run()
